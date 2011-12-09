%define		mod_name	encoding
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: convert character encoding of request URLs
Summary(pl.UTF-8):	Moduł Apache'a przekształcający kodowanie znaków żądanych URL-i
Name:		apache-mod_%{mod_name}
%define		_source_version	20021209
Version:	20040616
Release:	0.1
License:	Apache or BSD-like?
Group:		Networking/Daemons/HTTP
Source0:	http://webdav.todo.gr.jp/download/mod_%{mod_name}-%{_source_version}.tar.gz
# Source0-md5:	489cbd9c7429baf45c4234c51cb2af23
Source1:	http://webdav.todo.gr.jp/download/experimental/mod_%{mod_name}.c.apache2.%{version}
# Source1-md5:	5015b7a38e16be8534d2edcc8614d00e
#Source1:	%{name}.conf
#Source2:	%{name}.logrotate
Patch0:		%{name}-iconv_h.patch
URL:		http://webdav.todo.gr.jp/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		_pkglogdir	%(%{apxs} -q PREFIX 2>/dev/null)/logs

%description
This module improves non-ascii filename interoperability of Apache
(and mod_dav).

%description -l pl.UTF-8
Ten moduł poprawia współpracę Apache'a (i mod_dav) z nazwami plików
zawierającymi znaki spoza ASCII.

%prep
%setup -q -n mod_%{mod_name}-%{_source_version}
install %{SOURCE1} mod_%{mod_name}.c
#%patch0 -p0

%build
%{__autoconf}
%{__aclocal}
%{__automake}
%configure \
	--with-apxs=%{apxs}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir},/etc/logrotate.d,%{_pkglogdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README*
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
#%attr(755,root,root) %{_pkglibdir}/*.so
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
#%attr(640,root,root) %ghost %{_pkglogdir}/*
