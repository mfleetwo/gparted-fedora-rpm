Summary: Gnome Partition Editor
Name:    gparted
Version: 0.0.9
Release: 3
Group:   Applications/System
License: GPL
URL:     http://gparted.sourceforge.net
Source0: http://dl.sf.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gtkmm24-devel parted-devel 
BuildRequires: e2fsprogs-devel gettext
BuildRequires: desktop-file-utils

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to
libparted. Among other features it supports creating, resizing, moving
and copying of partitions. Also several (optional) filesystem tools provide
support for filesystems not included in libparted. These optional packages
will be detected at runtime and don't require a rebuild of GParted

%prep
%setup -q

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

#### consolehelper stuff (stolen from extras' synaptic)
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/gparted %{buildroot}%{_sbindir}/
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

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/gparted
%{_sbindir}/gparted
%{_datadir}/applications/fedora-gparted.desktop
%{_datadir}/pixmaps/gparted.png
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted

%changelog
* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-3
- Use correct source url

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-2
- Add more buildrequires and cleanup spec file

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-1
- Update to latest released version

* Wed Oct 26 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.8-1
- initial Extras release