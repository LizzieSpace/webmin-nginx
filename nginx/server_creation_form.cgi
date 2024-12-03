#!/usr/bin/perl
# create_server.cgi
# Create a new virtual host.

require './nginx-lib.pl';

&ui_print_header(undef, $text{'server_create'}, "");

#plain open document creation here
print &ui_form_start("create_server.cgi", "form-data");

print &ui_table_start($text{'index_create'}, undef, 2);
print &ui_table_row("Server Name",
  &ui_textbox("newserver", undef, 40));

print &ui_table_row("Config",
  &ui_textarea("directives", undef, 25, 80, undef, undef,"style='width:100%'"));

print &ui_table_row("",
  &ui_submit($text{'save'}));

print &ui_table_end();
print &ui_form_end();

&ui_print_footer("", $text{'index_return'});
