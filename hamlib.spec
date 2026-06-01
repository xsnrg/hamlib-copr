%global tclver 9.0   # kept for reference, but Tcl binding is disabled

Name:           hamlib
Version:        4.7.1
Release:        1%{?dist}
Summary:        Run-time library to control radio transceivers and receivers

License:        GPL-2.0-or-later and LGPL-2.0-or-later
URL:            https://hamlib.github.io/
Source0:        https://github.com/Hamlib/Hamlib/releases/download/%{version}/%{name}-%{version}.tar.gz

ExcludeArch:    i686

BuildRequires:  automake autoconf libtool
BuildRequires:  make
BuildRequires:  gcc gcc-c++
BuildRequires:  gd-devel
BuildRequires:  doxygen
BuildRequires:  source-highlight
BuildRequires:  boost-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libusb1-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)

# Filter provides from private libraries.
%{?perl_default_filter}

%description
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

%package devel
Summary:        Development library to control radio transceivers and receivers
Requires:       hamlib%{?_isa} = %{version}-%{release}

%description devel
Hamlib radio control library C development headers and libraries
for building C applications with Hamlib.

%package doc
Summary:        Documentation for the hamlib radio control library
BuildArch:      noarch

%description doc
This package provides the developers documentation for the hamlib radio
control library API.

%package c++
Summary:        Hamlib radio control library C++ binding
Requires:       hamlib%{?_isa} = %{version}-%{release}

%description c++
Hamlib radio control library C++ language binding.

%package c++-devel
Summary:        Hamlib radio control library C++ binding development headers and libraries
Requires:       hamlib-devel%{?_isa} = %{version}-%{release}
Requires:       hamlib-c++%{?_isa} = %{version}-%{release}

%description c++-devel
Hamlib radio control library C++ binding development headers and libraries
for building C++ applications with Hamlib.

%package -n perl-%{name}
Summary:        Hamlib radio control library Perl binding
Requires:       hamlib%{?_isa} = %{version}-%{release}
Obsoletes:      hamlib-perl < 3.0
Provides:       hamlib-perl = %{version}-%{release}

%description -n perl-%{name}
Hamlib PERL Language bindings to allow radio control from PERL scripts.

%package -n python3-%{name}
Summary:        Hamlib radio control library Python binding
Requires:       hamlib%{?_isa} = %{version}-%{release}, python3

%description -n python3-%{name}
Hamlib Python Language bindings to allow radio control from Python scripts.

# Tcl binding completely disabled (prevents packaging failures on rawhide)
# %package -n tcl-%{name}
# ...

%prep
%autosetup -p1 -n hamlib-%{version}

%build
%if 0%{?fedora} || 0%{?rhel} >= 8
export PYTHON=%{__python3}
%else
export PYTHON=%{__python2}
%endif

# === CUSTOM COMPILE FLAGS GO HERE (uncomment and edit as needed) ===
# export CFLAGS="${CFLAGS} -O3 -march=native -flto"
# export CXXFLAGS="${CXXFLAGS} -O3 -march=native -flto"
# export LDFLAGS="${LDFLAGS} -flto"

%configure \
        --disable-static \
        --with-perl-binding \
        --with-python-binding \
        --without-tcl-binding   # Tcl binding disabled

%make_build

# Build Documentation
make -C doc doc

%install
%make_install

# Install documentation
mkdir -p %{buildroot}%{_docdir}/%{name}/html/search
for f in `find doc/html/ -type f -maxdepth 1`; do
    install -D -m 0644 $f %{buildroot}%{_docdir}/%{name}/`echo $f | cut -d '/' -f2`
done
for f in `find doc/html/search -type f -maxdepth 1`; do
    install -D -m 0644 $f %{buildroot}%{_docdir}/%{name}/html/`echo $f | cut -d '/' -f3`
done

# Move installed docs to include them in subpackage via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv %{buildroot}%{_docdir}/%{name}/* __tmp_doc

# Fix permissions
find %{buildroot} -type f -name Hamlib.so -exec chmod 0755 {} ';'

# Remove unneeded files
find %{buildroot} -name \*.la -exec rm -f {} ';'
find %{buildroot} -type f -name pkgIndex.tcl -exec rm -f {} ';'
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name Hamlib.bs -exec rm -f {} ';'
find %{buildroot} -type f -name perltest.pl -exec rm -f {} ';'

%check
make V=1 check

%ldconfig_scriptlets

%ldconfig_scriptlets c++

%files
%license COPYING
%doc AUTHORS ChangeLog PLAN README THANKS
%{_bindir}/*
%{_libdir}/libhamlib.so.*
%{_mandir}/man?/*

%files devel
%doc README.developer
%{_libdir}/libhamlib.so
%{_datadir}/aclocal/hamlib.m4
%dir %{_includedir}/hamlib
%{_includedir}/hamlib/ampclass.h
%{_includedir}/hamlib/amplifier.h
%{_includedir}/hamlib/amplist.h
%{_includedir}/hamlib/multicast.h
%{_includedir}/hamlib/rig.h
%{_includedir}/hamlib/riglist.h
%{_includedir}/hamlib/rig_dll.h
%{_includedir}/hamlib/rotator.h
%{_includedir}/hamlib/rotlist.h
%{_libdir}/pkgconfig/hamlib.pc

%files doc
%doc __tmp_doc/*

%files c++
%{_libdir}/libhamlib++.so.*

%files c++-devel
%{_libdir}/libhamlib++.so
%{_includedir}/hamlib/rigclass.h
%{_includedir}/hamlib/rotclass.h

%files -n perl-%{name}
%{_libdir}/perl5/vendor_perl/auto/Hamlib
%{_libdir}/perl5/vendor_perl/Hamlib.pm

%files -n python3-%{name}
%{python3_sitearch}/Hamlib*

%changelog
* Mon Jun 01 2026 Jim <kf0sbp@proton.me> - 4.7.1-1
- Update to 4.7.1 (Tcl binding disabled for compatibility)
