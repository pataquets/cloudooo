##############################################################################
#
# Copyright (c) 2002-2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Gabriel M. Monnerat <gabriel@tiolive.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from zope.interface import implements
from cloudooo.interfaces.application import IApplication
from cloudooo.utils import logger, socketStatus
from psutil import pid_exists, Process


class Application(object):
  """Base object to create an object that is possible manipulation a
  process"""

  implements(IApplication)

  name = "application"

  def start(self):
    """Start Application"""
    logger.debug("Process Started %s, Port %s. Pid %s" % (self.name,
                                                    self.getAddress()[-1],
                                                    self.pid()))

  def stop(self):
    """Stop the process"""
    if hasattr(self, 'process') and self.status():
      process_pid = self.process.pid
      logger.debug("Stop Pid - %s" % process_pid)
      try:
        self.process.terminate()
      finally:
        if pid_exists(process_pid) or self.status():
          Process(process_pid).kill()

  def loadSettings(self, hostname, port, path_run_dir, display_id, **kwargs):
    """Define attributes for application instance
    Keyword arguments:
    hostname -- Host to start the instance.
    port -- Expected a int number.
    path_run_dir -- Full path to create the enviroment.
    display_id -- Display to open the OpenOffice.
    """
    self.hostname = hostname
    self.port = port
    self.path_run_dir = path_run_dir
    self.display_id = display_id
    self.timeout = kwargs.get('start_timeout', 20)

  def restart(self):
    """Start and Stop the process"""
    self.stop()
    self.start()

  def status(self):
    """Check by socket if the openoffice work."""
    return socketStatus(self.hostname, self.port)

  def getAddress(self):
    """Return port and hostname of OOo Instance."""
    return self.hostname, self.port

  def pid(self):
    """Returns the pid"""
    if not hasattr(self, 'process') or not self.status():
      return None
    return self.process.pid
