#!/usr/bin/perl -w

use strict;
use utf8;

my $APP='/Applications/1Password.app';
my $BAKEXT='.orig';

my @FILES=(
	{ File => 'Contents/Resources/datatypes/2904-login.js',
	  Content => q({
  "class":"wallet.computer.LoginInformation",
  "contents":[
    {
      "set":"",
      "disclosed":"yes",
      "fields":[
        { "name":"hostname", "type":"string" },
        { "name":"service", "type":"string" },
        { "name":"username", "type":"string" },
        { "name":"password", "type":"concealed" }
      ]
    }
  ]
}
)
	},
	{ File => 'Contents/Resources/English.lproj/DetailView/standard/wallet.computer.LoginInformation.html',
	  Content => q(<h1><img class="titleIcon" src="[template.baseURL]/WalletIcon.png" width="32" height="32" alt="Secure Note" />[object.title.html]<input type="button" class="editTop" value="Edit" onclick="javascript:controller.editObject('[object.uuid]')" /></h1>

<div class="contentPadding">

<p class="notes"><span class="label">Notes:</span>[object.notesHTML]</p>

<p>
  
<table class="dynamicFields" cellpadding="0" cellspacing="0">
  <tr>
    <th><span class="name">Hostname:</span></td>
    <td><span class="value">[object.secureContents.hostname.html]</span></td>
  </tr>
  <tr>
    <th><span class="name">Service:</span></td>
    <td><span class="value">[object.secureContents.service.html]</span></td>
  </tr>
  <tr>
    <th><span class="name">Username:</span></td>
    <td><span class="value"><a class="copy" href='javascript:controller.copyToClipboardFieldOfObject("secureContents.username", "[object.uuid]")'>[object.secureContents.username.html]<span class="copyButton">Copy</span></a></span></td>
  </tr>
  <tr>
    <th><span class="name">Password:</span></td>
    <td><span class="value"><a class="copy" href='javascript:controller.copyToClipboardFieldOfObject("secureContents.password", "[object.uuid]")'>[object.secureContents.password.concealed.html] <span class="copyButton">Copy</span></a></span></td>
  </tr>
</table></p>
</p>
<p><span class="label">Created: [object.createdAt] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Last modified on: [object.updatedAt]</span></p>
</div>
)
	},
       );

my $LOCALIZABLE_FILE = 'Contents/Resources/English.lproj/Localizable.strings';
my $LOCALIZABLE_STRINGS = q("wallet.computer.LoginInformation" = "Login Information";
"wallet.computer.LoginInformation.desc" = "Generic login information.";
"wallet.computer.LoginInformation.hostname" = "Hostname";
"wallet.computer.LoginInformation.service" = "Service";
"wallet.computer.LoginInformation.username" = "Username";
"wallet.computer.LoginInformation.password" = "Password";
);

# Quit 1password
print "Quitting 1Password...\n";
system(q(osascript -e 'tell application "1Password" to quit' >/dev/null 2>&1));

# Make a backup of the application
print "Making a backup of the application...\n";
system("rm -rf $APP$BAKEXT");
if (system("cp -Rp $APP $APP$BAKEXT") != 0) {
  die "Something happened while making a copy of the application - aborting for safety\n";
}

# Add the new files
for my $file (@FILES) {
  my $fname=$file->{File};
  my $content=$file->{Content};
  print "Writing $fname...\n";
  my $file="$APP/$fname";
  if (-f $file) {
    die "   $fname already exists - aborting\n";
  }
  open F, ">$file" or die "Error opening $file for writing\n";
  print F $content;
  close F or die "Error closing $file\n";
}

# Add the localizable strings

print "Adding strings to Localizable.strings...\n";
my $file="$APP/$LOCALIZABLE_FILE";
#open F, ">>$file" or die "Error opening $file for append\n";
# Modification for UTF16 contributed by Damon Cortesi (http://dcortesi.com/)
open F, ">>:raw:perlio:encoding(utf16be)", $file or die "Error opening $file for append\n";
print F $LOCALIZABLE_STRINGS;
close F or die "Error closing $file\n";

print "Done\n";
