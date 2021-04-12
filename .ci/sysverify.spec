%define _binaries_in_noarch_packages_terminate_build   0
Name: sysverify
Version: 3.0
Release: %{buildid}
Summary: SysVerify RPM to perform OS level Checks. Tag - cmi
Packager: Andrew Jones
Group: DevOps
License: GPL
Source0: sysverify.tar
BuildArch: noarch
Nosource: 0
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Requires: gcc
Requires: python
Requires: PyYAML
AutoReq: yes

%description
This Package will Install sysverify Components under /usr/local/script. Command to perform the Sysverify test -- (./sysverify). Gitlab commit ID: %{commitid}

%prep
%setup -n sysverify

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/local/script
mkdir -p $RPM_BUILD_ROOT/etc/sysverify.d
install test.yaml $RPM_BUILD_ROOT/etc/sysverify.d/test.yaml
install sysverify $RPM_BUILD_ROOT/usr/local/script/sysverify

%files
%defattr(-,root,root,-)
%attr(755,root,root)/usr/local/script/sysverify
%attr(755,root,root)/etc/sysverify.d/test.yaml
/etc/sysverify.d
/usr/local/script
/usr/local/script/sysverify

%clean
rm -rf $RPM_BUILD_ROOT

### Installation is selected ###
%post
if [ "$1" = "1" ]; then
    #cd /tmp/Sysverify/sysverify
    #chmod 744 /tmp/Sysverify/sysverify/sysverify
    #cp /tmp/Sysverify/sysverify/sysverify /usr/local/script/
    #cp /tmp/Sysverify/sysverify/test2.yaml /etc/sysverify.d/
    chmod 755 /usr/local/script/sysverify
fi

### Uninstallation is selected ###
%preun
if [ "$1" = "0" ]; then
    rm -rf /usr/local/script/sysverify >/dev/null 2>&1
    rm -f /etc/sysverify.d/test.yaml
fi

### Post uninstall section ###
%postun
if [ "$1" = 0 ] ### Post uninstall section ###
then
   touch /tmp/uninstall.txt
   echo " sysverify Package has been uninstalled.." >/tmp/uninstall.txt
fi
