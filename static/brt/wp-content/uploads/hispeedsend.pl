#!/usr/bin/perl
# Send an SMS message through the hispeed.ch web service.
# You need your cablecom login and password.
# Diego Zamboni, June 13, 2008.

use WWW::Mechanize;
use Getopt::Long;

######################################################################
# Preconfigured login info if you don't want to specify it every time
my $login='';
my $pass='';
######################################################################

my $usage="$0 [--login login] [--pass=pass] phonenum message";

GetOptions("login=s" => \$login,
	"pass=s" => \$pass);

my $dst=shift @ARGV;
my $msg="@ARGV";

die "$usage\n" unless $login && $pass && $dst && $msg;

my $mech=WWW::Mechanize->new();

$mech->get('https://your.hispeed.ch/fr/apps/messenger/');

my $resp=$mech->submit_form(
		   form_name => 'anmeldung',
		   fields => {
			      mail => $login,
			      password => $pass,
			     }
		  );

$mech->get('https://your.hispeed.ch/glue.cgi?http://messenger.hispeed.ch/walrus/app/login.do?language=fr');

$mech->submit_form(
		  form_name => 'smsBean',
		  fields => {
			     message => $msg,
			     numCount => length($msg),
			     originator => 'originatorUser',
			     recipientChecked => 'yes',
			     recipient => $dst,
			    },
		  );

1;
