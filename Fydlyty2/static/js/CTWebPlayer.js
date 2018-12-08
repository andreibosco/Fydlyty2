// CrazyTalk WebPlayer API v1.01.0210.1
// Reallusion Inc. (c) 2014 All rights reserved.


function CTWebPlayer( setting ) {
	if ( undefined === setting ) setting = {};
	if ( undefined === setting.params )	setting.params = {};
	if ( undefined === setting.params.logoimage ) {
		setting.params.logoimage = "http://ctinteractive.reallusion.com/ctinteractive/ctweblogo.png";
	}
	this.enableGoogleAnalytics = (undefined === setting.enableGoogleAnalytics)? true:setting.enableGoogleAnalytics;
	if( document.location.protocol != 'https:' &&
		document.location.protocol != 'http:' ){
	    this.enableGoogleAnalytics = false;
	}
	this.u = new UnityObject2(setting);			//unity object
	this.playerUrl = "http://ctinteractive.reallusion.com/ctinteractive/1.0/CTWebPlayer.unity3d?v=1002111";
	this.root = null;							//player jQuery object
	this.handleInstall = ( undefined === setting.handleInstall )? true : setting.handleInstall;
	this.logo = setting.params.logoimage;
	if ( this.enableGoogleAnalytics ) {	//setup google
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','//www.google-analytics.com/analytics.js','ga');	
	}
	// if ( !Object.prototype.hasOwnProperty ) {
	// Object.prototype.hasOwnProperty = function(prop) {
		// var proto = this.__proto__ || this.constructor.prototype;
		// return (prop in this) && (!(prop in proto) || proto[prop] !== this[prop]);
	// }};
}

CTWebPlayer.prototype.init = function( node, handler ) {

	this.root = (node.nodeType)? node : node.get(0);
	this.name = this.root.id;
	var callback = handler;
	var callbackFail = undefined;
	if ((typeof handler) == 'object') {
		callback = null;
		if ( handler.playerUrl ) {
			this.playerUrl = handler.playerUrl;
		}
		if ( handler.loaded ) {
			callback = handler.loaded;
		}
		if ( handler.error ) {
			callbackFail = handler.error;
		}
	}
	var uP  = this;
	var url = window.location.host + window.location.pathname;
	this.u.observeProgress( function (progress) {	
			
		if ( progress.pluginStatus=="first" ) {		
			uP.u.getUnity().SendMessage( "RL_API", "SetPlayerHtmlPath", url );
  		    uP.u.getUnity().SendMessage( "RL_API", "ShowPlayBar", 1 );
			if( callback ){
				callback( progress );
			}
		} else {
			if ( uP.handleInstall ) {
				
				if ( progress.pluginStatus=="unsupported" ) {
					var strHtml = "<div style=\"width:100%;height:";
						strHtml += $(uP.root).height()/4;
						strHtml += "px;margin:auto;\"></div>";
						strHtml += "<img src=\"";
						strHtml	+= uP.logo;
						strHtml += "\" /><p>Sorry, the CrazyTalk player cannot be supported by your current browser.\
									<a href=\"http://www.reallusion.com/linkcount/linkcount.aspx?lid=ci1en13\" target=\"_blank\">more...</a></p>";
					$( uP.root ).html(strHtml);									
					$( uP.root ).css("background-color", "white");					
				} else if ( progress.pluginStatus=="missing" ) {
					var strHtml = "<div style=\"width:100%;height:";
						strHtml += ($(uP.root).height()-63)/2;
						strHtml += "px;margin:auto;\"></div>";
						strHtml += "<a href=\"http://unity3d.com/webplayer/\" target=\"_blank\">\
										<img src=\"http://webplayer.unity3d.com/installation/getunity.png\" width=\"193\" height=\"63\" />\
									</a>";
					$( uP.root ).html(strHtml);	
				}
			}
			if ( callbackFail ) callbackFail( progress );
		}
		
	});	
	this.u.initPlugin( this.root, this.playerUrl );	
	if ( this.enableGoogleAnalytics ) {	//send data to google analytics
		ga('create', 'UA-7053738-8', 'reallusion.com');
		ga('send', 'pageview');
		ga('send', 'event', url,'CTWebPlayer',  'website');
	}
	
}
CTWebPlayer.prototype.setCameraMode = function( mode ) {
	var cameraMode = 0;
	if ( mode == "standard" ) {
		cameraMode = 1;
	} else if ( mode == "telephoto" ) {
		cameraMode = 2;
	}
	this.u.getUnity().SendMessage( "RL_API", "SetCameraPerspective", cameraMode );
}
CTWebPlayer.prototype.genCallbackName = function( param ) {
	if ( param && param.name && (param.name in window) ) return param.name;
	var name = this.root.id + "_callback";
	var num = 0;
	while ( name in window ) {	// generate unique name for unity3d to callback
		name = this.root.id + "_callback" + num;
		num++;
	}
	window[ name ] = param;
	return name;
}
CTWebPlayer.prototype.loadProject = function( url, settings ) {
	
	var callback = null;
	var alphaActor = 1;
	var alphaBG = 1;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.playAfter === undefined ) { settings.playAfter = -1; }
	if ( settings.showActor == false ) { alphaActor = 0; }
	if ( settings.showBackground == false ) { alphaBG = 0; }
	if ( settings.idleMotionUrl === undefined ) { settings.idleMotionUrl = null; }
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadProject", 
	[url, settings.playAfter, alphaActor, alphaBG, settings.idleMotionUrl, callback] );
}
CTWebPlayer.prototype.loadActor = function( url, settings ) {
	
	var callback = null;
	var alphaActor = 1;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.showActor == false ) { alphaActor = 0; }
	if ( settings.idleMotionUrl === undefined ) { settings.idleMotionUrl = null; }	
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );		
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadCharacter", [url, alphaActor, settings.idleMotionUrl, callback] );
}
CTWebPlayer.prototype.loadMotion = function( url, settings ) {
	
	var callback = null;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.playAfter === undefined ) { settings.playAfter = -1; }
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );				
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadMotion", [url, settings.playAfter, callback] );
}
CTWebPlayer.prototype.loadScript = function( url, settings ) {
	
	var callback = null;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.playAfter === undefined ) { settings.playAfter = -1; }
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );						
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadScript", [url, settings.playAfter, callback] );
}
CTWebPlayer.prototype.loadIdleMotion = function( url, loaded ) {
	
	var callback = null;
	if ( loaded ) {
		callback = this.genCallbackName( settings.loaded );						
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadIdleMotion", [url, callback] );
}
CTWebPlayer.prototype.loadBackground = function( url, settings ) {
	
	var callback = null;
	var fit = 0;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.alpha === undefined ) { settings.alpha = 1.0; }
	if ( settings.fit == "fill" ) { 
		fit = 1; 
	}
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );						
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadBackGroundImage", [url, settings.alpha, fit, callback] );
}
CTWebPlayer.prototype.loadForeground = function( url, settings ) {
	
	var fit = 0;
	var callback = null;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.name  === undefined ) { settings.name = "Foreground" }
	if ( settings.zOrder === undefined ) { settings.zOrder = 0 }
	if ( settings.alpha === undefined ) { settings.alpha = 1.0; }
	if ( settings.fit == "fill" ) { fit = 1; } else if ( settings.fit == "stretch" ) { fit = 2; }
	if ( settings.x === undefined ){ settings.x = 0; }
	if ( settings.y === undefined ){ settings.y = 80; }
	if ( settings.width === undefined ){ settings.width = 100; }
	if ( settings.height === undefined ){ settings.height = 20; }	
	if ( settings.linkUrl !== undefined ){ settings.action = "parent.location.href = \""+settings.linkUrl+"\""; }
	if ( settings.hotspotX === undefined ){ settings.hotspotX = 0; }
	if ( settings.hotspotY === undefined ){ settings.hotspotY = 0; }
	if ( settings.hotspotWidth === undefined ){ settings.hotspotWidth = 100; }
	if ( settings.hotspotHeight === undefined ){ settings.hotspotHeight = 100; }
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );						
	}
	this.u.getUnity().SendMessage( "RL_API", "LoadForeGroundImage", [url, settings.name, settings.zOrder, settings.alpha, fit, callback, settings.x/100.0, settings.y/100.0, settings.width/100.0, settings.height/100.0, 
	settings.action, settings.hotspotX/100.0, settings.hotspotY/100.0, settings.hotspotWidth/100.0, settings.hotspotHeight/100.0] );
}
CTWebPlayer.prototype.preLoadFiles = function( urls, settings ) {
	
	var callback = null;
	if ( settings === undefined ) { settings = {}; }
	if ( settings.thread === undefined ) { settings.thread = 2; }
	if ( settings.loaded ) {
		callback = this.genCallbackName( settings.loaded );						
	}
	this.u.getUnity().SendMessage( "RL_API", "PreloadFiles", [urls, settings.thread, callback] );
}
CTWebPlayer.prototype.play = function( delay ) {
	
	if ( delay === undefined ) { delay = 0.0; }
	this.u.getUnity().SendMessage( "RL_API", "Play", delay );
}
CTWebPlayer.prototype.stop = function( delay ) {
	
	if ( delay === undefined ) { delay = 0.0; }
	this.u.getUnity().SendMessage( "RL_API", "Stop", delay );
}
CTWebPlayer.prototype.pause = function( delay ) {
	
	if ( delay === undefined ) { delay = 0.0; }
	this.u.getUnity().SendMessage( "RL_API", "Pause", delay );
}
CTWebPlayer.prototype.setLoop = function( loop ) {
	
	loop = ( ( loop === undefined ) || !loop )? 0 : 1; 
	this.u.getUnity().SendMessage( "RL_API", "SetPlayBackMode", loop );
}
CTWebPlayer.prototype.setVolume = function( volume ) {
	
	var value = volume / 100.0;
	this.u.getUnity().SendMessage( "RL_API", "SetAudioVolume", value );
}
CTWebPlayer.prototype.showPlaybar = function( show ) {
	if ( show === undefined ) { show = true; }
	this.u.getUnity().SendMessage( "RL_API", "ShowPlayBar", (!show)?0:1 );
}
CTWebPlayer.prototype.showProgressbar = function( show ) {
	if ( show === undefined ) { show = true; }	
	this.u.getUnity().SendMessage( "RL_API", "ShowProgressBar", (!show)?0:1 );
}
CTWebPlayer.prototype.showForeground = function( name, show, duration ) {
	if ( show === undefined ) { show = true; }	
	this.u.getUnity().SendMessage( "RL_API", "ShowForeGround", [ name, (!show)?0:1, (!duration)?0.0:duration] );
}
CTWebPlayer.prototype.showBackground = function( show, duration ) {
	if ( show === undefined ) { show = true; }	
	this.u.getUnity().SendMessage( "RL_API", "ShowBackGround", [(!show)?0:1, (!duration)?0.0:duration] );
}
CTWebPlayer.prototype.showActor = function( show, duration ) {
	if ( show === undefined ) { show = true; }
	this.u.getUnity().SendMessage( "RL_API", "ShowActor", [(!show)?0:1, (!duration)?0.0:duration] );
}
CTWebPlayer.prototype.setLookat = function( mode ) {
	var value = 0;
	if ( mode == "player" ) {
		value = 1;
	} else if ( mode == "screen" ) {
		value = 2;
	}
	this.u.getUnity().SendMessage( "RL_API", "SetLookAtMode", value );
}
CTWebPlayer.prototype.setLookatStrength = function( mode ) {
	var value = 0.8;
	if ( mode == "mild" ) {
		value = 0.4;
	} else if ( mode == "strong" ) {
		value = 1.2;
	}
	this.u.getUnity().SendMessage( "RL_API", "SetLookatStrength", value );
}
CTWebPlayer.prototype.actorTransform = function( settings ) {
	if ( settings.scale === undefined ) {
		settings.scale = 100;
	}
	if ( settings.duration === undefined ) {
		settings.duration = 0.0;
	}
	this.u.getUnity().SendMessage( "RL_API", "ActorTransform", [settings.duration,settings.positionX,settings.positionY,settings.scale,settings.scale] );
}
CTWebPlayer.prototype.actorGaze = function( settings ) {
	this.u.getUnity().SendMessage( "RL_API", "ActorGaze", [settings.degree,settings.radius,settings.duration] );
}
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? 
    [ parseInt(result[1], 16), parseInt(result[2], 16), parseInt(result[3], 16) ] : null;
}
CTWebPlayer.prototype.setBackgroundColor = function( color ) {
	
	var value = [ 0, 0, 0, 1 ];
	if ((typeof color) == 'object') {
		value = [ color.r, color.g, color.b, 1 ];
	} else if ((typeof color) == 'string') {
		value = hexToRgb( color );
		value[3] = 1;	
	}
	this.u.getUnity().SendMessage( "RL_API", "SetBackGroundColor", value );
}
CTWebPlayer.prototype.setBgDisplayMode = function( mode ) {
	var param = 0;
	if( mode == "fit" ){
	    value = 0;
	}else if( mode == "fill" ){
	    value = 1;
	}
	this.u.getUnity().SendMessage( "RL_API", "SetFitBackgroundMode", value );
}
function toMouseEvent( button, shift, x, y ) {
	var event = { button:0, shiftKey:false, ctrlKey:false, clientX:x, clientY:y };
	if ( button == 1 ) {
		event.button = 2;
	} else if ( button == 2 ) {
		event.button = 1;
	}
	switch ( shift )
	{
	case 0:
		event.shiftKey = true;
		break;
	case 1:
		event.ctrlKey = true;
		break;
	case 2:
		event.shiftKey = true;
		event.ctrlKey = true;
		break;
	}
	return event;
}
function toPlayerEvent( url, status, time, length ) {
	return { url:url, status:status, time:time, length:length };
} 
CTWebPlayer.prototype.bind = function( event, handler ) {
	var callback = this.genCallbackName();	
	var callbackUser = callback + '_user';
	switch (event) {
	case "mousedown":
	case "mouseup":
	case "mousemove":
	case "click":
	case "dbclick":
		window[ callback ] = function( button, shift, x, y ) {
			window[ callbackUser ]( toMouseEvent( button, shift, x, y ) );
		};
		break;
	case "playerstatus":
		window[ callback ] = function( url, status, time, length ) {
			window[ callbackUser ]( toPlayerEvent( url, status, time, length ) );
		};	
		break;
	default:
		return;
	};
	window[ callbackUser ] = handler;	
	this.u.getUnity().SendMessage( "RL_API", "addEventLisener", [ event, callback ] );
	if ( !( event in window ) ) {
		this[event] = [];
	}
	this[event].push( callback );
	this[event].push( callbackUser );		
	//console.log( "add bind:" + callback + "event:" + event );	
}
CTWebPlayer.prototype.unbind = function( event ) {
	if ( event in this ) {
		for ( var key in this[event] ) {
			//console.log( "delete bind:" + this[event][key] );
			window[ this[event][key] ] = undefined;	// for IE
			try {
				delete window[ this[event][key] ];
			}catch(e){}
		}
		delete this[ event ];
	}
	this.u.getUnity().SendMessage( "RL_API", "removeEventLisener", event );
}