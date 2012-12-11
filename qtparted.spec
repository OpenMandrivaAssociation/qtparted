%bcond_with qt_embedded
%bcond_with kapabilities

Name:		qtparted
Version:	0.6.0
Release:	1
Summary:	Graphical Partitioning Tool
License:	GPL
Group:		System/Kernel and hardware
URL:		http://qtparted.sf.net/
Source:		http://freefr.dl.sourceforge.net/project/qtparted/qtparted-%version/qtparted-%version.tar.xz
Source10:	qtparted.pamd
Source11:	qtparted.pam
Patch0:		qtparted-desktop.patch
BuildRequires:	cmake
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(libparted)
Requires:	qtparted-data = %{version}-%{release}
Provides:	%{name}-ui = %{version}-%{release}

%description
QtParted is a graphical partition editor, similar to PartitionMagic(tm).

%package data
Summary:	Data files common to qtparted and qtparted-nox
Group:		System/Kernel and hardware
BuildArch:	noarch
Requires:	%{name}-ui = %{version}-%{release}

%description data
Data files common to qtparted and qtparted-nox.

%package nox
Summary:	A version of the QtParted partition editor that runs without X11
Group:		System/Kernel and hardware
Requires:	%{name}-data = %{version}-%{release}
Provides:	%{name}-ui = %{version}-%{release}

%description nox
A version of the QtParted partition editor that runs without X11.

%prep
%setup -q
%patch0 -p0

%build
# Actual build happens in %%install so we can install 2 different copies
# (linked against Qt-X11 and Qt-Embedded)

%install
%if %{with qt_embedded}
cmake -DQT_QMAKE_EXECUTABLE=%{_libdir}/qt4-embedded/bin/qmake -DQT_RPATH:BOOL=TRUE -DCMAKE_INSTALL_PREFIX=%{_prefix} .
%make

%makeinstall_std
make clean
find . -name "CMakeCache.txt" |xargs rm -f
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-nox
%endif

cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} .
#cmake_qt4
%make

%makeinstall_std

%if %{with kapabilities}
# pam/kapabilities support
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
ln -s consolehelper %{buildroot}%{_bindir}/qtparted
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/qtparted
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
install -m 644 -D %{SOURCE11} %{buildroot}%{_sysconfdir}/security/console.apps/qtparted
%endif

%files
%if %{with kapabilities}
%{_sbindir}/qtparted
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%endif
%{_bindir}/*
%{_datadir}/applications/*

%files data
%{_datadir}/%{name}
%{_datadir}/pixmaps/*

%if %{with qt_embedded}
%files nox
%{_sbindir}/qtparted-nox
%endif

