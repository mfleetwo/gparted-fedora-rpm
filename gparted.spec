Summary: Gnome Partition Editor
Name:    gparted
Version: 0.4.8
Release: 1%{?dist}
Group:   Applications/System
License: GPLv2+
URL:     http://gparted.sourceforge.net
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:  gparted-epel-build-workaround.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gtkmm24-devel parted-devel 
BuildRequires: e2fsprogs-devel gettext perl(XML::Parser) 
BuildRequires: desktop-file-utils gnome-doc-utils
BuildRequires:  scrollkeeper
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to
libparted. Among other features it supports creating, resizing, moving
and copying of partitions. Also several (optional) filesystem tools provide
support for filesystems not included in libparted. These optional packages
will be detected at runtime and don't require a rebuild of GParted

%prep
%setup -q
%patch0 -p0 -b .epel

%build
%configure
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

sed -i 's#_X-GNOME-FullName#X-GNOME-FullName#' %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --delete-original                   \
        --vendor fedora                                  \
        --dir %{buildroot}%{_datadir}/applications       \
	--mode 0644				         \
        %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i 's#sbin#bin#' %{buildroot}%{_datadir}/applications/fedora-%{name}.desktop

rm -rf %{buildroot}/var

#### consolehelper stuff
mkdir -p %{buildroot}%{_bindir}
ln -s consolehelper %{buildroot}%{_bindir}/gparted

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/gparted
USER=root
PROGRAM=%{_sbindir}/gparted
SESSION=true
FALLBACK=false
EOF

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cat << EOF > %{buildroot}%{_sysconfdir}/pam.d/gparted
#%PAM-1.0
auth       sufficient   /%{_lib}/security/pam_rootok.so
auth       sufficient   /%{_lib}/security/pam_timestamp.so
auth       required     /%{_lib}/security/pam_stack.so service=system-auth
session    required     /%{_lib}/security/pam_permit.so
session    optional     /%{_lib}/security/pam_xauth.so
session    optional     /%{_lib}/security/pam_timestamp.so
account    required     /%{_lib}/security/pam_permit.so
EOF

%find_lang %{name}

%clean
rm -rf %{buildroot}

%preun
if [ $1 -ge 0 ]; then
    if [ -a %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi ]; then
       rm -rf %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi
    fi
fi

%post
scrollkeeper-update -q -o %{_datadir}/omf/%{name} || :

touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
scrollkeeper-update -q || :

touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/gparted
%{_sbindir}/gparted
%{_sbindir}/gpartedbin
%{_datadir}/applications/fedora-gparted.desktop
%{_datadir}/icons/hicolor/*/apps/gparted.*
%{_datadir}/gnome/help/gparted/
%{_datadir}/omf/gparted/
%{_mandir}/man8/gparted.*
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted

%changelog
* Mon Jan 18 2010 Deji Akingunola <dakingun@gmail.com> - 0.4.8-1
- New upstream version
- Remove the hal policy file created by gparted (if it's still there)
 on upgrade (Should fix BZ #550590)

* Sun Dec 16 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-4
- Branch off for EL-5
- Apply a couple of patches from F-7 branch
- Remove the X-Fedora category form the desktop file

* Mon Jun 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-3
- Apply patch to only detect real devices, useful for correcting gparted slow 
 startup in situations when floppy drives doesn't exist but are enabled in bios
 (BZ #208821).

* Wed Mar 07 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-2
- Rebuild

* Thu Dec 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.3-1
- Bug fix release

* Tue Dec 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.2-1
- New release

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
