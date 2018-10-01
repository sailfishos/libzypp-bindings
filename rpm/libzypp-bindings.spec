# 
# spec file for package libzypp-bindings
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
# 
# nodebuginfo
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%if 0%{?suse_version}
%{!?ruby_vendorarch: %define ruby_vendorarch %(ruby -rrbconfig -e 'puts Config::CONFIG["vendorarchdir"] ')}
%else
%{!?ruby_vendorarch: %define ruby_vendorarch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}
%endif

Name:           libzypp-bindings
Version:        0.7.4
Release:        1.3
License:        GPL v2 or later
Summary:        Bindings for libzypp
Group:          Development/Sources
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake gcc-c++ python-devel
BuildRequires:  swig >= 1.3.40
BuildRequires:  libzypp-devel

%description
This package provides bindings for libzypp, the library for package management.

%prep
%setup -q -n %{name}-%{version}/upstream

%build
rm -rf build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{prefix} \
      -DPYTHON_SITEDIR=%{python_sitearch} \
      -DLIB=%{_lib} \
      -DCMAKE_VERBOSE_MAKEFILE=TRUE \
      -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
      -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_SKIP_RPATH=1 \
      -DBUILD_PERL5_BINDINGS=OFF \
      -DBUILD_RUBY_BINDINGS=OFF \
      ..

make -j1

%check
cd build
make test

%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT

%clean

%package -n python-zypp
Summary:        Python bindings for libzypp
Group:          Development/Languages/Python
%description -n python-zypp
Python bindings of libzypp

%files -n python-zypp
%defattr(-,root,root,-)
%{python_sitearch}/_zypp.so
%{python_sitearch}/zypp.py*
