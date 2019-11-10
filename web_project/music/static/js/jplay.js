$(document).ready(function() {
	$.ajax({
		url: "http://127.0.0.1:8000/music/list/",
		type: "get",
		success: function(response) {
			console.log(response);
			new jPlayerPlaylist(
				{
					jPlayer: "#jquery_jplayer_2",
					cssSelectorAncestor: "#jp_container_2"
				},
				response,
				{
					swfPath:
						"https://cdnjs.cloudflare.com/ajax/libs/jplayer/2.9.2/jplayer/jquery.jplayer.swf",
					supplied: "oga, mp3",
					wmode: "window",
					useStateClassSkin: true,
					autoBlur: false,
					smoothPlayBar: true,
					keyEnabled: true
				}
			);
		}
	});
});
