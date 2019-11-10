$(document).ready(function() {
	/*
	 * Instance CirclePlayer inside jQuery doc ready
	 *
	 * CirclePlayer(jPlayerSelector, media, options)
	 *   jPlayerSelector: String - The css selector of the jPlayer div.
	 *   media: Object - The media object used in jPlayer("setMedia",media).
	 *   options: Object - The jPlayer options.
	 *
	 * Multiple instances must set the cssSelectorAncestor in the jPlayer options. Defaults to "#cp_container_1" in CirclePlayer.
	 */

	var myCirclePlayer = [];

	$.ajax({
		url: "http://127.0.0.1:8000/music/list/",
		type: "get",
		success: function(response) {
			console.log(response);
			for (i in response) {
				console.log("i", i, response[i]);
				myCirclePlayer.concat(
					new CirclePlayer(
						"#jquery_jplayer_".concat(i),
						{
							m4a: response[i].m4a,
							oga: response[i].oga,
							mp3: response[i].mp3
						},
						{
							cssSelectorAncestor: "#cp_container_".concat(i)
						}
					)
				);
			}
		}
	});

	// This code creates a 2nd instance. Delete if not required.

	// This code creates a 2nd instance. Delete if not required.

	var myOtherOne = new CirclePlayer(
		"#jquery_jplayer_2",
		{
			m4a: "Miaow-04-Lismore.m4a",
			oga: "http://www.jplayer.org/audio/ogg/Miaow-04-Lismore.ogg"
		},
		{
			cssSelectorAncestor: "#cp_container_2"
		}
	);
});
