%{!?python_site: %define python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

Name:           xpd
Version:        0.3.3
Release:        1%{?dist}
Summary:        Infineon e-bike controller setup tool
Group:          Applications/Engineering
License:        GPLv3+
URL:            http://xpd.berlios.de/
Source0:        http://download.berlios.de/xpd/xpd-%{version}.tar.bz2
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  python
BuildRequires:  desktop-file-utils
Requires:       python pygtk2 pyserial
Requires:       desktop-file-utils

%description
XPD is a cross-platform replacement for the widely known in close circles
Parameter Design tool (also known as Keywin e-Bike Lab), used to set the
parameters of a e-bike controller based on the Infineon XC846 microcontroller
(and various clones).

%prep
%setup -q

%build
# nothing to do :)

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc debian/changelog README TRANSLATORS
%{python_site}/%{name}m/*
%{python_site}/%{name}-%{version}*-info
%{_bindir}/xpd
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_datadir}/%{name}/*

%post
update-desktop-database -q

%postun
update-desktop-database -q

%changelog
* Fri Aug 12 2011 Andrey Zabolotnyi <zap@cobra.ru> - 0.2.1-1
- Updated source to version 0.2.1

* Sat Jun 4 2011 Andrey Zabolotnyi <zap@cobra.ru> - 0.2.0-1
- Get rid of the glade dependency, now using gtk.Builder

* Mon May 2 2011 Andrey Zabolotnyi <zap@cobra.ru> - 0.1.0-1
- First version of the spec file
