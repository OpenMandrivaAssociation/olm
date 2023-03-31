# For the python module - it doesn't link to libpython
%define _disable_ld_no_undefined 1

%define major %(echo %{version} |cut -d. -f1)
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary: Double Ratchet cryptographic library
Name: olm
Version: 3.2.14
Release: 2
License: ASL 2.0
Group: System/Libraries
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

%package -n %{libname}
Summary: Double Ratchet cryptographic library
Group: System/Libraries

%description -n %{libname}
An implementation of the Double Ratchet cryptographic ratchet in C++.

%description -n %{libname}
Double Ratchet cryptographic library

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C++
Requires: %{libname}%{?_isa} = %{EVRD}
Provides: %{name}-devel = %{EVRD}

%description -n %{devname}
Devel Olm packages for Double Ratchet cryptographic library

%package python
Summary: Python 3 bindings for %{name}
Group: Development/Python
Requires: %{libname}%{?_isa} = %{?EVRD}

%description python
Python 3 bindings for Olm Double Ratchet cryptographic library

%prep
%autosetup -p1
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DOLM_TESTS=OFF \
    -G Ninja

%build
%ninja_build -C build

export CFLAGS="%{optflags} -L$(pwd)/build/%{_lib}"
export LDFLAGS="%{build_ldflags} -L$(pwd)/build/%{_lib}"
cd python
%py_build

%check
cd build
ctest --output-on-failure

%install
%ninja_install -C build

cd python
%py_install
cd ..

%files -n %{libname}
%license LICENSE
%doc *.md *.rst docs/*.md
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/Olm
%{_libdir}/pkgconfig/olm.pc

%files python
%{python_sitearch}/%{name}
%{python_sitearch}/_lib%{name}.abi3.so
%{python_sitearch}/python_%{name}-*.egg-info
