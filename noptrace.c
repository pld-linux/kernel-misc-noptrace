/*
 * noptrace kernel module.
 *
 * Copyright Brian Hatch, 2001. Released under the GPL.
 * taken from http://www.hackinglinuxexposed.com/tools/p/noptrace.c
 * modified by BartOwl to NOT taint the 2.4 kernels
 *
 * Disable the ptrace system call entirely.  Used
 * to help prevent attacks against setuserid binaries
 * on pre 2.2.19 kernels, which have a massive security
 * problem.
 *
 * NOTE: This defends against only one avenue of
 * attack for the vulnerable kernels, however most
 * script-kiddie exploits are using the ptrace
 * vulnerability, so this is a good first step.
 *
 * It will probably be useful in the future, as I am sure
 * we'll find a few more ptrace-exploitable bugs down the
 * road.
 *
 * Install this at your own risk.  We suggest you
 * read the LKM chapters of Hacking Linux Exposed for
 * discussion about how loadable kernel modules work
 * where we discuss some in detail.
 *
 * To compile:
 *    gcc -o noptrace.o -c noptrace.c
 *
 * Then copy noptrace.o into one of the default
 * insmod directories, such as /lib/modules/misc.
 *
 * Load it into the running kernel with 'insmod noptrace'.
 *
 */

#define __KERNEL__
#define MODULE

#include <linux/config.h>
#include <linux/module.h>
#include <linux/version.h>
#include <sys/syscall.h>

#include <linux/sched.h>
#include <linux/types.h>

#ifdef MODULE_LICENSE
MODULE_LICENSE("GPL");
#endif

int (*real_ptrace) (int, int, int, int);
int new_ptrace  (int, int, int, int);
extern void *sys_call_table[];

int init_module() {

      /* Save a pointer to the old ptrace function */
      real_ptrace   = sys_call_table[ __NR_ptrace ];

      /* point to our new ptrace function in sys_call_table */
      sys_call_table[ __NR_ptrace ]   =  (void *)new_ptrace;

      printk(KERN_INFO "noptrace module installed\n");
      return 0;
}

int cleanup_module() {

      /* reset the pointer back to the actual function */
      sys_call_table[ __NR_ptrace ]   = (void *)real_ptrace;

      printk(KERN_INFO "noptrace module uninstalled\n");
        return 0;
}


/* The replacement function */

int new_ptrace(int request, int pid, int addr, int data) {
      return current->euid ?
	      -1:
	      (real_ptrace)(request, pid, addr, data);
}

