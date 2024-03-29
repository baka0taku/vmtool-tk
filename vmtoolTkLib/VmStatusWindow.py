'''
Window to display critical VM stats for a selected VM
CPU usage, RAM usage, Disk Usage, Frozen?, Power state?, Snapshots?, VMDK Files
'''
from .FuncLib import *


class VmStatusWindow:
    def __init__(self, dataset: DataTree):
        self.data: DataTree = dataset
        self.cpuvar: StringVar = StringVar()
        self.ramvar: StringVar = StringVar()
        self.disknumvar: StringVar = StringVar()
        self.diskusevar: StringVar = StringVar()
        self.diskfilevar: StringVar = StringVar()
        self.frozenvar: StringVar = StringVar()
        self.powervar: StringVar = StringVar()
        self.snapvar: StringVar = StringVar()

        # define widgets
        self.top_level = Toplevel(master=self.data.rootwin)
        self.vm_frame = Frame(master=self.top_level)
        self.vm_list = Listbox(master=self.vm_frame, width=50, height=15)
        self.vm_scroll = Scrollbar(master=self.vm_frame, orient=VERTICAL)
        self.cpu_label = Label(master=self.top_level, text="CPU Usage")
        self.cpu_usage = Label(master=self.top_level, relief=SUNKEN, textvariable=self.cpuvar)
        self.mem_label = Label(master=self.top_level, text="Memory Usage")
        self.mem_usage = Label(master=self.top_level, relief=SUNKEN, textvariable=self.ramvar)
        self.disk_usage_label = Label(master=self.top_level, text="Disk Usage")
        self.disk_usage = Label(master=self.top_level, relief=SUNKEN, textvariable=self.diskusevar)
        self.power_label = Label(master=self.top_level, text="Powered on?")
        self.power = Label(master=self.top_level, relief=SUNKEN, textvariable=self.powervar)
        self.frozen_label = Label(master=self.top_level, text="Frozen?")
        self.frozen = Label(master=self.top_level, relief=SUNKEN, textvariable=self.frozenvar)
        self.num_disks_label = Label(master=self.top_level, text="Number of Disks")
        self.num_disks = Label(master=self.top_level, relief=SUNKEN, textvariable=self.disknumvar)
        self.num_snapshots_label = Label(master=self.top_level, text="Number of Snapshots")
        self.num_snapshots = Label(master=self.top_level, relief=SUNKEN, textvariable=self.snapvar)
        self.num_disk_files_label = Label(master=self.top_level, text="Number of Disk Files/Disk")
        self.num_disk_files = Label(master=self.top_level, relief=SUNKEN, textvariable=self.diskfilevar)







        # define scrollbar properties
        self.vm_list.config(yscrollcommand=self.vm_scroll.set)
        self.vm_scroll.config(command=self.vm_list.yview)

        # add VMs to list
        self.vm_list.insert(END, *sorted(list(self.data.vmdict.keys())))

        # place widgets
        self.vm_frame.grid(column=0, row=0, padx=20, pady=20, rowspan=8)
        self.vm_list.pack(side=LEFT)
        self.vm_scroll.pack(side=RIGHT, fill=BOTH)
        self.cpu_label.grid(column=1, row=0, padx=10, pady=10)
        self.cpu_usage.grid(column=2, row=0, padx=10, pady=10)
        self.mem_label.grid(column=1, row=1, padx=10, pady=10)
        self.mem_usage.grid(column=2, row=1, padx=10, pady=10)
        self.disk_usage_label.grid(column=1, row=2, padx=10, pady=10)
        self.disk_usage.grid(column=2, row=2, padx=10, pady=10)
        self.power_label.grid(column=1, row=3, padx=10, pady=10)
        self.power.grid(column=2, row=3, padx=10, pady=10)
        self.frozen_label.grid(column=1, row=4, padx=10, pady=10)
        self.frozen.grid(column=2, row=4, padx=10, pady=10)
        self.num_disks_label.grid(column=1, row=5, padx=10, pady=10)
        self.num_disks.grid(column=2, row=5, padx=10, pady=10)
        self.num_snapshots_label.grid(column=1, row=6, padx=10, pady=10)
        self.num_snapshots.grid(column=2, row=6, padx=10, pady=10)
        self.num_disk_files_label.grid(column=1, row=7, padx=10, pady=10)
        self.num_disk_files.grid(column=2, row=7, padx=10, pady=10)



        #event handler
        def list_handle(event) -> None:
            # get selected index
            selected_index: tuple = self.vm_list.curselection()

            # get vm name from listbox
            selected_name: str = self.vm_list.get(selected_index)

            # get vm object from dictionary
            vm_object: vim.VirtualMachine = self.data.vmdict.get(selected_name)

            # get data from object about VM
            self.cpuvar.set(get_cpu_usage(vm_object))
            self.ramvar.set(get_memory_usage(vm_object))
            self.diskusevar.set(get_disk_usage(vm_object))
            if is_powered_on(vm_object):
                self.powervar.set("Yes")
            else:
                self.powervar.set("No")
            if is_frozen(vm_object):
                self.frozenvar.set("Yes")
            else:
                self.frozenvar.set("No")
            self.disknumvar.set(get_num_disks(vm_object))
            self.snapvar.set(get_num_snapshots(vm_object))
            self.diskfilevar.set(get_num_disk_files(vm_object))

            return

        #event binding
        self.vm_list.bind('<<ListboxSelect>>', list_handle)


