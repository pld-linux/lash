Summary:	LASH Audio Session Handler
Summary(pl.UTF-8):	LASH Audio Session Handler - obsługa sesji dźwiękowych
Name:		lash
Version:	0.5.4
Release:	8
License:	GPL v2+
Group:		Applications/Sound
Source0:	http://download.savannah.gnu.org/releases/lash/%{name}-%{version}.tar.gz
# Source0-md5:	8eeb7e91f9127d7d9fc6ec076cbe14ed
Patch0:		%{name}-link.patch
Patch1:		%{name}-glibc2.8.patch
Patch2:		%{name}-swig2.patch
Patch3:		texinfo5.patch
Patch4:		rlimit.patch
Patch5:		%{name}-swig3.patch
Patch6:		%{name}-linking.patch
URL:		http://lash.nongnu.org/
BuildRequires:	/usr/bin/texi2html
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.99.17
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig3-python
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LASH Audio Session Handler consists of a daemon, a client library and
a some clients that implement a session management system for audio
applications on Linux.

%description -l pl.UTF-8
LASH Audio Session Handler składa się z demona, biblioteki klienckiej
i kilku programów klienckich implementujących system zarządzania
sesjami dla aplikacji dźwiękowych działających pod Linuksem.

%package gtk
Summary:	GTK+ based LASH clients
Summary(pl.UTF-8):	Programy klienckie LASH oparte na GTK+
Group:		X11/Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}

%description gtk
GTK+ based LASH clients.

%description gtk -l pl.UTF-8
Programy klienckie LASH oparte na GTK+.

%package libs
Summary:	LASH Audio Session Handler library
Summary(pl.UTF-8):	Biblioteka LASH Audio Session Handler
Group:		Libraries

%description libs
LASH Audio Session Handler library.

%description libs -l pl.UTF-8
Biblioteka LASH Audio Session Handler do obsługi sesji dźwiękowych.

%package devel
Summary:	Header files for LASH library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LASH
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libuuid-devel

%description devel
Header files for LASH library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LASH.

%package static
Summary:	Static LASH library
Summary(pl.UTF-8):	Statyczna biblioteka LASH
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LASH library.

%description static -l pl.UTF-8
Statyczna biblioteka LASH.

%package -n python-lash
Summary:	Python bindings for LASH library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LASH
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-lash
Python bindings for LASH library.

%description -n python-lash -l pl.UTF-8
Wiązania Pythona do biblioteki LASH.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p0
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	SWIG=/usr/bin/swig-3
%{__make} \
	pkgpyexecdir="\$(pyexecdir)"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgpyexecdir="\$(pyexecdir)"

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_lash.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.SECURITY TODO docs/lash-manual-html-split/lash-manual*
%attr(755,root,root) %{_bindir}/lash_control
%attr(755,root,root) %{_bindir}/lash_simple_client
%attr(755,root,root) %{_bindir}/lash_synth
%attr(755,root,root) %{_bindir}/lashd
%{_datadir}/lash

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lash_panel
%attr(755,root,root) %{_bindir}/lash_save_button

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblash.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblash.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblash.so
%{_libdir}/liblash.la
%{_includedir}/lash-1.0
%{_pkgconfigdir}/lash-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblash.a

%files -n python-lash
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_lash.so
%{py_sitedir}/lash.py[co]
