%bcond_with kapabilities

%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Name:		qtparted
Version:	0.7.0
Release:	3
Summary:	Graphical Partitioning Tool
License:	GPL
Group:		System/Kernel and hardware
URL:		http://qtparted.sf.net/
Source0:	http://freefr.dl.sourceforge.net/project/qtparted/qtparted-%version/qtparted-%version.tar.xz
Source10:	qtparted.pamd
Source11:	qtparted.pam
Patch0:		qtparted-desktop.patch
BuildRequires:	cmake
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	pkgconfig(libparted)
# We obsolete -data and -nox for good, there's no need to do an
# X11 vs. Qt/Embedded split anymore with Qt5, and that need won't
# return. The dark ages are over :)
Obsoletes:	qtparted-data
Obsoletes:	qtparted-nox

%description
QtParted is a graphical partition editor, similar to PartitionMagic(tm).

%prep
%setup -q
%patch0 -p0 -b .desktop~
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}

%build
%make -C build

%install
%makeinstall_std -C build

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
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
