#
# Conditional build:
# _without_dist_kernel	- without distribution kernel
#

%define		_orig_name	noptrace

Summary:	Kernel module for disabling ptrace()
Summary(pl):	Modu� j�dra wy��czaj�cy ptrace()
Name:		kernel-misc-%{_orig_name}
# Is there any version???
Version:	0.1
%define	_rel	6
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.hackinglinuxexposed.com/tools/p/%{_orig_name}.c
# NoSource0-md5: a6f1ea1f4842caa43d720c532b8a1c18
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	%{kgcc_package}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kernel module for disabling ptrace() system call.

%description -l pl
Modu� kernela wy��czaj�cy wywo�anie systemowe ptrace().

%package -n kernel-smp-misc-%{_orig_name}
Summary:	SMP kernel module for disabling ptrace()
Summary(pl):	Modu� j�dra SMP wy��czaj�cy ptrace()
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-%{_orig_name}
SMP kernel module for disabling ptrace() system call.

%description -n kernel-smp-misc-%{_orig_name} -l pl
Modu� j�dra SMP wy��czaj�cy wywo�anie systemowe ptrace().

%prep
%setup -q -T -c
install %{SOURCE0} .

%build
%{kgcc} -D__KERNEL__ -DMODULE -D__SMP__ -DCONFIG_X86_LOCAL_APIC -I%{_kernelsrcdir}/include -Wall \
	-Wstrict-prototypes -fomit-frame-pointer -fno-strict-aliasing -pipe -fno-strength-reduce \
	%{rpmcflags} -c %{_orig_name}.c

mv -f %{_orig_name}.o %{_orig_name}smp.o

%{kgcc} -D__KERNEL__ -DMODULE -I%{_kernelsrcdir}/include -Wall -Wstrict-prototypes \
	-fomit-frame-pointer -fno-strict-aliasing -pipe -fno-strength-reduce \
	%{rpmcflags} -c %{_orig_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
cp %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp %{_orig_name}smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-misc-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-misc-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-%{_orig_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
