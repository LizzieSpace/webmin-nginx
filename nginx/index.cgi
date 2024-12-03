#!/usr/bin/perl
# index.cgi
# Display a list of all virtual servers, and links for various types

use HTML::Entities;
require './nginx-lib.pl';
&ReadParse();

# add virtual servers
my @virts = &get_servers();
foreach my $v (@virts) {
  # $idx = &indexof($v, @$conf);
  my $sn = basename($v);
  my $status = '<span style="color:darkgreen">' . $text{'status_enabled'} . '</span>';
  if (!-e "$config{'link_dir'}/$sn") {
    $status = $text{'status_disabled'};
  }
  push(our @vidx, $sn);
  push(our @vstatus, "$status");
  push(our @vname, $sn);
  push(our @vlink, "edit_server.cgi?editfile=$sn");
  push(our @vroot, &find_directives($v, 'root'));
  push(our @vurl, encode_entities(&find_directives($v, 'server_name')));
}

# Page header
&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, undef,
  &help_search_link("nginx", "man", "doc", "google"), undef, undef,
  &text('index_version', $nginfo{'version'}));

print '<div style="background:#fffdba; padding:10px; margin:20px 0;">' . $config{'messages'} . '</div>' if $config{'messages'};
$config{'messages'} = '';
save_module_config();
&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Global settings

print &ui_subheading($text{'index_global'});
my $global_icon = {
  "icon" => "images/nginx_edit.png",
  "name" => $text{'gl_edit'},
  "link" => "edit_server.cgi?editfile=$config{'nginx_conf'}"
};
my $proxy_icon = {
  "icon" => "images/edit_proxy.png",
  "name" => $text{'gl_proxy'},
  "link" => "edit_server.cgi?editfile=proxy.conf"
};
my $det_icon = {
  "icon" => "images/nginx_details.png",
  "name" => $text{'gl_details'},
  "link" => "details.cgi"
};
&config_icons($global_icon, $proxy_icon, $det_icon);
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Virtual Servers Table

print &ui_hr();

print &ui_subheading($text{'index_virts'});
my @links;
  push(
      @links,
      &select_all_link("d"),
      &select_invert_link("d"),
  );
  print &ui_form_start("update_server.cgi", "get");
  print &ui_columns_start([
    $text{'index_select'},
    $text{'index_status'},
    $text{'index_name'},
#     $text{'index_addr'},
#     $text{'index_port'},
    $text{'index_root'},
    $text{'index_url'} ], 100);
  for(my $i=0; $i<@vname; $i++) {
    my @cols;
    push(@cols, "$vstatus[$i]");
    push(@cols, "<a href=\"$vlink[$i]\">$vname[$i]</a>");
#     push(@cols, &html_escape($vaddr[$i]));
#     push(@cols, &html_escape($vport[$i]));
    push(@cols, &html_escape($vroot[$i]));
    push(@cols, "<a href=\"//$vurl[$i]\">$vurl[$i]</a>");
    print &ui_checked_columns_row(\@cols, undef,"d", $vidx[$i]);
  }
  print &ui_columns_end();
  print &ui_links_row(\@links);
  print &ui_select("action", "",
    [ ['_none', $text{'opt_select'}], ['enable', $text{'opt_enable'}], ['disable', $text{'opt_disable'}], ['delete', $text{'opt_delete'}] ]);
  print &ui_form_end([ [ "submit", $text{'btn_submit'} ] ]);

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Show start / stop buttons
print &ui_hr();

print &ui_buttons_start();
print &ui_buttons_row(
    "server_creation_form.cgi",
    $text{'index_create'}
);
if (&is_nginx_running()) {
    print &ui_buttons_row(
        "stop.cgi",
        $text{'index_stop'},
        $text{'index_stopdesc'});
	print &ui_buttons_row(
        "reload.cgi",
        $text{'index_restart'},
        $text{'index_restartdesc'});
	}
else {
	print &ui_buttons_row(
        "start.cgi",
        $text{'index_start'},
        $text{'index_startdesc'});
	}
print &ui_buttons_end();

ui_print_footer("/", $text{'index'});
