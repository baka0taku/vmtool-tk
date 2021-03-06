"""
    GUI for status window - for the most part just creates the GUI window. Most of the heavy lifting is done in Vulcan.
    This file contains an exception. For some reason that i haven't ferreted out yet attempting to move the data parsing
    to Vulcan causes it to break with circular dependencies.

    -=baka0taku=-
"""

from pyVmomi import vim
from vmtoolTkLib.FuncLib import *


class StatWindow:
    def __init__(self, data: DataTree) -> None:
        # assign data to object
        self.dataset = data
        # create new window
        self.statWin = Toplevel(master=self.dataset.rootwin, bg='black')

        # define widgets
        self.container = Frame(master=self.statWin, bg='black', padx=20, pady=20)
        self.statlab = Label(master=self.container, text='Getting contents of vCenter...', bg='black', fg='white')
        # place widgets
        self.statlab.grid(row=0, column=0, pady=20, sticky=E + W)
        self.container.pack(expand=True, fill=BOTH, padx=30, pady=30)
        self.statWin.update()
        self.parse_data()
        sleep(1)
        self.statWin.destroy()

    def parse_data(self) -> None:
        # get all content
        self.dataset.content = self.dataset.connection.RetrieveContent()
        # get all VMs
        self.dataset.vmobjlist = self.dataset.content.viewManager.CreateContainerView(self.dataset.content.rootFolder,
                                                                                      [vim.VirtualMachine], True)
        for vm in self.dataset.vmobjlist.view:
            self.dataset.vmdict[vm.name] = vm
        # get all hosts
        self.dataset.hostobjlist = self.dataset.content.viewManager.CreateContainerView(self.dataset.content.rootFolder,
                                                                                        [vim.HostSystem], True)
        for host in self.dataset.hostobjlist.view:
            self.dataset.hostdict[host.name] = host
        # get all datastores
        self.dataset.datastoreobjlist = self.dataset.content.viewManager.CreateContainerView(
            self.dataset.content.rootFolder,
            [vim.Datastore], True)
        for ds in self.dataset.datastoreobjlist.view:
            self.dataset.datastoredict[ds.name] = ds
        # get all networks
        self.dataset.networkobjlist = self.dataset.content.viewManager.CreateContainerView(
            self.dataset.content.rootFolder,
            [vim.Network], True)
        for net in self.dataset.networkobjlist.view:
            if type(net) is vim.dvs.DistributedVirtualPortgroup:
                self.dataset.dvportgroupdict[net.name] = net
            else:
                self.dataset.networkdict[net.name] = net
        # get all dvswitches
        self.dataset.dvswitchobjlist = self.dataset.content.viewManager.CreateContainerView(
            self.dataset.content.rootFolder,
            [vim.DistributedVirtualSwitch], True)
        for dvs in self.dataset.dvswitchobjlist.view:
            self.dataset.dvswitchdict[dvs.name] = dvs
        return
