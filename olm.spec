%global appname olm

Name: olm
Version: 3.1.5
Release: 1

Summary: Double Ratchet cryptographic library
License: ASL 2.0
URL: https://gitlab.matrix.org/matrix-org/%{name}
Source0: https://gitlab.matrix.org/matrix-org/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires: ninja
BuildRequires: cmake

BuildRequires: pkgconfig(python)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(cffi)
BuildRequires: python3dist(future)

%description
An implementation of the Double Ratchet cryptographic ratchet in C++.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package python
Summary: Python 3 bindings for %{name}
%{?python_provide:%python_provide python3-%{appname}}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Devel Olm packages for Double Ratchet cryptographic library

%description python
Python 3 bindings for Olm Double Ratchet cryptographic library

%prep
%autosetup -n %{appname}-%{version} -p1

%build
    %cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DOLM_TESTS=OFF \
    -G Ninja
   
%ninja_build

cd python

#pushd python
%py_build
popd

%check
pushd %{_target_platform}/tests
    ctest --output-on-failure
popd

%install
%ninja_install -C %{_target_platform}

pushd python
%py_install
popd

%files
%license LICENSE
%doc *.md *.rst docs/*.md
%{_libdir}/%{name}.so.3*

%files devel
%{_includedir}/%{appname}
%{_libdir}/%{name}.so
%{_libdir}/cmake/Olm

%files python
%{python_sitearch}/%{appname}
%{python_sitearch}/_%{name}.abi3.so
%{python_sitearch}/python_%{appname}-*.egg-info
