%define up_name	ctypes
%define debug_package          %{nil}
# hacky workaround to be fixed!
%define __noautoreq '/usr/bin/ocamlrun'

Summary:	C type support for OCaml
Name:		ocaml-%{up_name}
Version:	0.3.3
Release:	5
Group:		Development/Other
License:	MIT-style
Url:            http://github.com/ocamllabs/ocaml-ctypes
Source0:        https://github.com/ocamllabs/ocaml-ctypes/archive/%{version}.tar.gz
Patch0:		ocaml-ctypes-0.3.3-compile.patch
BuildRequires:  ocaml-compiler
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-camlp4
BuildRequires:	ocaml-findlib
BuildRequires:	pkgconfig(libffi)
Requires:       ocaml-compiler = %(rpm -q --qf '%{VERSION}' ocaml-compiler)
Obsoletes:      %{up_name}

%description
ctypes is a library for binding to C libraries using pure OCaml.
The primary aim is to make writing C extensions as straightforward as possible.

The core of ctypes is a set of combinators for describing the structure of C
types -- numeric types, arrays, pointers, structs, unions and functions.
You can use these combinators to describe the types of the functions that you
want to call, then bind directly to those functions -- all without writing or
generating any C!

%package	devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%autopatch -p1
sed -i -e "s,\$(OCAMLFIND) install,\$(OCAMLFIND) install -destdir %{buildroot}$(ocamlfind printconf destdir) -ldconf ignore,g" Makefile
%make configure
touch setup.data

%build
# As of 0.3.3, Makefiles aren't SMP safe
make

%install
mkdir -p %{buildroot}$(ocamlfind printconf destdir)
# As of 0.3.3, Makefiles aren't SMP safe
make install
find %{buildroot}

%files
%dir %{_libdir}/ocaml/ctypes
%{_libdir}/ocaml/ctypes/*.cma
%{_libdir}/ocaml/ctypes/*.cmi
%{_libdir}/ocaml/ctypes/*.cmxs
%{_libdir}/ocaml/ctypes/*.so
%{_libdir}/ocaml/ctypes/META

%files devel
%{_libdir}/ocaml/ctypes/*.a
%{_libdir}/ocaml/ctypes/*.cmx
%{_libdir}/ocaml/ctypes/*.cmxa
%{_libdir}/ocaml/ctypes/*.h
%{_libdir}/ocaml/ctypes/*.mli

%post
grep -qE '^%{_libdir}/ocaml/ctypes$' %{_libdir}/ocaml/ld.conf || echo '%{_libdir}/ocaml/ctypes' >>%{_libdir}/ocaml/ld.conf

%postun
if [ "$1" = "0" ]; then
	sed -i -e '/^%(echo %{_libdir}/ocaml/ctypes |sed -e "s,/,\\\/,g")$/d' %{_libdir}/ocaml/ld.conf
fi
