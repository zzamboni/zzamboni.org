eval 'exec perl -x $0 ${1+"$@"}' # -*-perl-*-
  if 0;
#!perl -w
# Convert old AppMenu to the new XML format

print qq(<?xml version="1.0"?>\n);
print "<AppMenu>\n";
while (<>) {
  chomp;
  ($opt, $label)=split ' ', $_, 2;
  unless ($opt && $label) {
    warn "missing opt or label, skipping line: $_\n";
    next;
  }
  print qq(  <Item label="$label" option="--$opt"/>\n);
}
print "</AppMenu>\n";

