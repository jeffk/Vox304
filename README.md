# Vox304

A kinda complex twitter bot that renders the homepage of a random Vox Media site through a proxy in Netscape Navigator 3.04 running under MacOS 7.5.3 in Basilisk II. I'll leave it as an extercise for the user to get a working Basilisk II setup going, but Googling for a Quadra 605 ROM should help. Since Vox Media is all HTTPS now, the local proxy is used to rewrite HTTP requests into HTTPS ones, and strip out HTML and CSS that Navigator 3.04 can't handle. There are a lot of things hard-coded into this, but hopefully the code will be enough to get you started.

Online at [@vox304](http://twitter.com/vox304)

If you have questions on setting up your own, ping me on twitter [@jeffk](http://twitter.com/jeffk).

Uses:

* [GetWindowID](https://github.com/smokris/GetWindowID)
* [Basilisk II](http://www.emaculation.com/doku.php/basiliskii_osx_setup)
* [Netscape Navigator 3.04](http://main.system7today.com/otherbrowsers.html)
* [Proxy2](https://github.com/inaz2/proxy2)
