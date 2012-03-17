
function personalize() {
	var correctPhoneHash1 = '60a1de7a8ed5393a3f39323d43e7cfcbf5148abc';
	/* with salt d786dff79a90 */
	var correctEmailHash1 = '7969eb81c67b7fa87b7518e00a6d438c944f4106';
	/* with salt b2832fa81995 */
	var correctEmailHash2 = '49893e15e435f0da563f0bdee2d2bc0bfd2001f1';
	/* with salt b2832fa81995 */
	var correctEmailHash3 = '5184c8ea13f195b5113ab3c6f0be83461da0bdda';
	/* with salt b2832fa81995 */

    /* Get all url vars*/
	var urlVars = getUrlVars();
	/*Locate vars for phone number display*/
	var phone_number = urlVars['phone_number'];
	var s1 = urlVars['s1'];
	/*Locate vars for email display*/
	var email = urlVars['email'];
	var s2 = urlVars['s2'];
	/*Locate vars for viewer display*/
	var iv = urlVars['v1'];
	var salt = urlVars['v2'];
	var ct = urlVars['v3'];

	$("#contact-info").hide();
	$("#phone_number_label").hide();
	$("#email_address_label").hide();

	if (phone_number != null) {
		var phone_number_hash = String(Crypto.SHA1(s1 + phone_number));
		if (phone_number_hash == correctPhoneHash1) {
			$("#contact-info").show();
			$("#phone_number_label").show();
			$("#phone_number").text(phone_number);
		}
	}
	if (email != null) {
		var email_hash = String(Crypto.SHA1(s2 + email));
		if ((email_hash == correctEmailHash1) ||
			(email_hash == correctEmailHash2) ||
			(email_hash == correctEmailHash3)) {
			$("#contact-info").show();
			$("#email_address_label").show();
			$("#email_address").text(email);
		}
	}
	if (iv != null && salt != null && ct != null) {
		var name = "";
		/*var vi_encrypted = sjcl.encrypt("ballsohard", vi);*/
		var vi_encrypted  = "\{\"iv\"\:\"" + iv + "\"\,\"salt\"\:\"" + salt + "\"\,\"ct\"\:\"" + ct + "\"\}";
		/*var vi_encrypted2 = "{\"iv\":\"puPAHFivE1QyZOuM/GoIyQ\",\"salt\":\"Jz9SJG6LljE\",\"ct\":\"wWdX3Qr5vyaK7TzR\"}";*/
		try {
		    name = sjcl.decrypt("ballsohard", vi_encrypted);
		} catch(error) {
		    name = "guest";
		}
		if (name != "") {
			alert("Hello, " + name + "! Welcome to my personal page.");
		}
	}
}

function getUrlVars()
{
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for(var i = 0; i < hashes.length; i++)
	{
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	return vars;
}