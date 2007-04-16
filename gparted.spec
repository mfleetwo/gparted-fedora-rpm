Summary: Gnome Partition Editor
Name:    gparted
Version: 0.3.3
Release: 9%{?dist}
Group:   Applications/System
License: GPL
URL:     http://gparted.sourceforge.net
Source0: http://dl.sf.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Source1: run-gparted
Source2: gparted-console.apps
Source3: gparted-pam.d
Patch0:	gparted-dont-lock-hal.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gtkmm24-devel parted-devel 
BuildRequires: e2fsprogs-devel gettext perl(XML::Parser) 
BuildRequires: desktop-file-utils
Requires: hal >= 0.5.9

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to
libparted. Among other features it supports creating, resizing, moving
and copying of partitions. Also several (optional) filesystem tools provide
support for filesystems not included in libparted. These optional packages
will be detected at runtime and don't require a rebuild of GParted

%prep
%setup -q
%patch -p0 -b .hal

%build
%configure
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

desktop-file-install --delete-original                   \
        --vendor fedora                                  \
        --dir %{buildroot}%{_datadir}/applications       \
	--mode 0644				         \
        --add-category X-Fedora                          \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

# Create a helper script to launch gparted using hal-lock
cp %{SOURCE1} %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_bindir}/run-gparted

#### consolehelper stuff
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/gparted %{buildroot}%{_sbindir}/
ln -s consolehelper %{buildroot}%{_bindir}/gparted

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/gparted

%find_lang %{name}

%clean
rm -rf %{buildroot}

%preun
if [ $1 -ge 0 ]; then
    if [ -a %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi ]; then
       rm -rf %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi
    fi
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/gparted
%{_bindir}/run-gparted
%{_sbindir}/gparted
%{_datadir}/applications/fedora-gparted.desktop
%{_datadir}/pixmaps/gparted.png
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted

%changelog
* Mon Apr 15 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-9
- Fix the typos and stupidity in the consolehelper and hal-lock files

* Mon Apr 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-8
- Explicitly require hal >= 0.5.9
- Remove the hal policy file created by gparted (if it's still there) on upgrade

* Mon Apr 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-7
- Patch gparted to not create a hal fdi file but use hal-lock instead, this will hopefully fix BZ #215657
- Clean up the spec file

* Wed Mar 21 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-6
- Rebuild for GNU parted-1.8.6

* Tue Mar 20 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-5
- Rebuild for GNU parted-1.8.5

* Wed Jan 24 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-4
- Re-write the consolehelpher stuff to work with latest pam

* Tue Jan 16 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-3
- The new parted is back, rebuild again

* Sat Jan 13 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-2
- Rebuild for new parted

* Thu Dec 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.3-1
- Bug fix release

* Tue Dec 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.2-1
- New release

* Mon Nov 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-5
- Add more BRs

* Mon Nov 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-4
- Complete fix for parted check and apply patch on configure.in

* Wed Nov 23 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-3
- Backport a fix from cvs to properly check for libparted version

* Mon Nov 21 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-2
- Rebuild for new parted

* Wed Sep 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-1
- New version 0.3.1

* Tue Sep 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.3-1
- New version 0.3

* Mon Aug 28 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.5-3
- Rebuild for FC6

* Mon May 22 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.5-2
- Rebuild

* Mon May 22 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.5-1
- Update to version 0.2.5

* Mon Apr 17 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.4-2
- Rebuild for new parted

* Wed Apr 12 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.4-1
- Update to newer version

* Thu Mar 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.3-1
- Update to newer version

* Mon Mar 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.2-1
- New release

* Mon Feb 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.2-2
- Rebuild for Fedora Extras 5

* Mon Jan 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.2-1
- New release

* Wed Jan 11 2006 Deji Akingunola <dakingun@gmail.com> - 0.1-1
- New release

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-3
- Use correct source url

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-2
- Add more buildrequires and cleanup spec file

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-1
- Update to latest released version

* Wed Oct 26 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.8-1
- initial Extras release
