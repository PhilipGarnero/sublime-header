
#
# Imports some modules.
#

import sublime, sublime_plugin, os, time, locale

#
# Simple class to ask project name.
#

class PromptHeaderCommand(sublime_plugin.WindowCommand):

  def run(self):
    label = "Type project name: "
    self.window.show_input_panel(label, "", self.on_done, None, None)

  def on_done(self, text):
    try:
      self.window.active_view().run_command("header", {"project": text})
    except ValueError:
      pass


class HeaderUpdater(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        try:
          edit = view.begin_edit()
          header = Header(view)
          new_line = header.get_comment()[1] + " Last update " + header.get_date() + " " + header.fullname
          region = view.find("Last update", 0)
          line = view.line(region)
          view.replace(edit, line, new_line)
        except Exception as e:
          print e
        finally:
          view.end_edit(edit)



class Header():
  #
  # /!\ Find how to get this from system!
  #
  result = os.popen("getent passwd `whoami` | cut -d ':' -f 5 | cut -d ',' -f 1")
  fullname = result.read()[:-1]

  #
  # Get comment type according language.
  #

  def __init__(self, view):
    self.view = view

  def get_comment(self):
    comments = {}

    comments['Default']      = ['  ', '  ', '  ']
    comments['JavaScript']   = ['/**', ' *', ' */']
    comments['CSS']          = ['/**', ' *', ' */']
    comments['C++']          = ['/*', '**', '*/']
    comments['Python']       = ['#', '#', '#']
    comments['CoffeeScript'] = ['#', '#', '#']
    comments['Ruby']         = ['#', '#', '#']
    comments['Makefile']     = ['##', '##', '##']
    comments['Perl']         = ['#!/usr/local/bin/perl -w', '##', '##']
    comments['ShellScript']  = ['#!/bin/sh', '##', '##']
    comments['HTML']         = ['<!--', ' ', '-->']
    comments['LaTeX']        = ['%%', '%%', '%%']
    comments['Lisp']         = [';;', ';;', ';;']
    comments['Java']         = ['//', '//', '//']
    comments['PHP']          = ['#!/usr/local/bin/php\n<?php', '//', '//']
    comments['Jade']         = ['//-', '//-', '//-']
    comments['Stylus']       = ['//', '//', '//']

    return comments[self.view.settings().get('syntax').split('/')[1]]

  #
  # Get file infos.
  #

  def get_file_infos(self):
    full = self.view.file_name().split('/')
    return [full.pop(), '/'.join(full)]

  #
  # Get email
  #

  def get_mail(self):
    return "<" + os.environ['USER'] + "@epitech.net>"

  #
  # Get date epitech-formated (e.g Thu Jan  3 00:22:41 2013)
  #

  def get_date(self):

    # TODO:
    # - replace 03 by  3
    # - get day and month in english

    return time.strftime("%a %b  %d %H:%M:%S %Y")

#
# Main class: create the epitech-style header.
#
class HeaderCommand(sublime_plugin.TextCommand):
  #
  # Generate header.
  #
  def generate(self, project):

    # get some infos

    helper = Header(self.view)
    header = ""
    comment = helper.get_comment()
    f = helper.get_file_infos()

    # generate the header

    header += comment[0] + '\n'
    header += comment[1] + " " + f[0] + " for " + project + " in " + f[1] + '\n'
    header += comment[1] + '\n'
    header += comment[1] + " Made by " + helper.fullname + '\n'
    header += comment[1] + " Login   " + helper.get_mail() + '\n'
    header += comment[1] + '\n'
    header += comment[1] + " Started on  " + helper.get_date() + " " + helper.fullname + '\n'
    header += comment[1] + " Last update " + helper.get_date() + " " + helper.fullname + '\n'
    header += comment[2] + '\n'

    return header

  #
  # Run command.
  #

  def run(self, edit, project):
    self.view.insert(edit, 0, self.generate(project))

class ProtectedHeaderMaker(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    try:
      edit = view.begin_edit()
      filename = Header(view).get_file_infos()[0]
      filename, fileExtension = os.path.splitext(filename)
      filename = "{0}_H_".format(filename).upper()
      if fileExtension == ".hh" or fileExtension == ".h":
        if view.find("#ifndef", 0) == None:
          view.insert(edit, view.size(), "\n#ifndef {0}\n# define {0}\n\n\n\n#endif /* {0} */".format(filename))
    except Exception as e:
      print e
    finally:
      view.end_edit(edit)