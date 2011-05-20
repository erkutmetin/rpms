# $Id$
# Authority: shuff
# Upstream: Tokuhiro Matsuno <tokuhirom$gmail,com>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name Test-SharedFork

Summary: Test forking
Name: perl-Test-SharedFork
Version: 0.16
Release: 1%{?dist}
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Test-SharedFork/

Source: http://search.cpan.org/CPAN/authors/id/T/TO/TOKUHIROM/Test-SharedFork-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl >= 5.8.0
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More)
BuildRequires: rpm-macros-rpmforge
Requires: perl >= 5.8.0
Requires: perl(Test::Builder) >= 0.32
Requires: perl(Test::More)

### remove autoreq Perl dependencies
%filter_from_requires /^perl.*/d
%filter_setup

%description
Test::SharedFork is a utility module for Test::Builder which allows you to use
fork(2) safely in your test cases.

%prep
%setup -n %{real_name}-%{version}

# damn it Dist::Zilla
#%{?el5:%{__perl} -pi -e '/.*ExtUtils::MakeMaker.*6\.31.*/ && s/6\.3\d/6.30/' Makefile.PL}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install
#%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}

# fix for stupid strip issue
#%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes META.yml README
%doc %{_mandir}/man?/*
%{perl_vendorlib}/Test/SharedFork.pm
%{perl_vendorlib}/Test/SharedFork/*
#%exclude %{perl_archlib}/perllocal.pod
%exclude %{perl_vendorarch}/auto/*/*/.packlist

%changelog
* Fri May 20 2011 Steve Huff <shuff@vecna.org> - 0.16-1
- Initial package.
