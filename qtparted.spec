%bcond_with qt_embedded
%bcond_with kapabilities

%define rel %nil
Name:		qtparted
Version:	0.6.0
Summary:	Graphical Partitioning Tool
URL:		http://qtparted.sf.net/
%if "%rel" != ""
Release:	0.%rel.1
Source:		qtparted-%rel.tar.xz
%else
Release:	1
Source:		http://freefr.dl.sourceforge.net/project/qtparted/qtparted-%version/qtparted-%version.tar.lz
%endif
Source10:	qtparted.pamd
Source11:	qtparted.pam
License:	GPL
Group:		System/Kernel and hardware
Requires:	qtparted-data = %version-%release
Provides:	%name-ui = %version-%release
BuildRequires:	pkgconfig(QtCore) pkgconfig(QtGui) pkgconfig(libparted)

%description
QtParted is a graphical partition editor, similar to PartitionMagic(tm).

%package data
Summary: Data files common to qtparted and qtparted-nox
Requires: %name-ui = %version-%release
Group: System/Kernel and hardware
BuildArch: noarch

%description data
%summary

%package nox
Summary: A version of the QtParted partition editor that runs without X11
Requires: %name-data = %version-%release
Group: System/Kernel and hardware
Provides: %name-ui = %version-%release

%description nox
A version of the QtParted partition editor that runs without X11

%prep
%if "%rel" != ""
%setup -q -n qtparted
%else
%setup -q -n %name-%version
%endif

%build
# Actual build happens in %%install so we can install 2 different copies
# (linked against Qt-X11 and Qt-Embedded)

%install
%if %{with qt_embedded}
cmake -DQT_QMAKE_EXECUTABLE=%_libdir/qt4-embedded/bin/qmake -DQT_RPATH:BOOL=TRUE -DCMAKE_INSTALL_PREFIX=%_prefix .
make %?_smp_mflags

make install DESTDIR="$RPM_BUILD_ROOT"
make clean
find . -name "CMakeCache.txt" |xargs rm -f
mv $RPM_BUILD_ROOT%_bindir/%name $RPM_BUILD_ROOT%_bindir/%name-nox
%endif


cmake -DCMAKE_INSTALL_PREFIX=%_prefix .
make %?_smp_mflags

make install DESTDIR="$RPM_BUILD_ROOT"

%if %{with kapabilities}
# pam/kapabilities support
mkdir -p %{buildroot}%{_sbindir}
mv %buildroot%_bindir/* %buildroot%_sbindir
mkdir -p %{buildroot}%{_bindir}
ln -s consolehelper %{buildroot}%{_bindir}/qtparted
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/qtparted
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
install -m 644 -D %{SOURCE11} %{buildroot}%{_sysconfdir}/security/console.apps/qtparted
%endif

%files
%defattr(-,root,root)
%if %{with kapabilities}
%{_sbindir}/qtparted
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%endif
%{_bindir}/*
%{_datadir}/applications/*

%files data
%defattr(-,root,root)
%{_datadir}/%name
%{_datadir}/pixmaps/*

%if %{with qt_embedded}
%files nox
%defattr(-,root,root)
%_sbindir/qtparted-nox
%endif

%clean
rm -rf $RPM_BUILD_ROOT
