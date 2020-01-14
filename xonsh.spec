Name:           xonsh
Version:        0.9.13
Release:        3%{?dist}
Summary:        A general purpose, Python-ish shell

# xonsh is BSD-2-Clause.
# xonsh/winutils.py and xonsh/xoreutils/_which.py contain MIT code.
License:        BSD and MIT
URL:            https://xon.sh
Source0:        %pypi_source
Source1:        65-xonsh.conf
Source2:        xonsh-session
Patch0:         xonsh-0.9.13-exec-well-behaviour.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  %{py3_dist ply}
BuildRequires:  %{py3_dist prompt-toolkit}
BuildRequires:  %{py3_dist pygments}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  git
BuildRequires:  man-db
Requires:       python3 >= 3.4
Requires:       %{py3_dist ply}
Requires:       %{py3_dist prompt-toolkit}
Requires:       %{py3_dist setproctitle}
Requires:       %{py3_dist pygments}
Requires:       %{py3_dist distro}


%description
xonsh is a Python-powered, cross-platform, Unix-gazing shell language and
command prompt. The language is a superset of Python 3.4+ with additional shell
primitives. xonsh (pronounced *conch*) is meant for the daily use of experts
and novices alike.

%prep
%autosetup -n %{name}-%{version}
%patch0 -p0

%build
# Remove shebang.
sed --in-place "s:#!\s*/usr.*::" xonsh/xoreutils/_which.py

%py3_build

%install
%py3_install

# py3_build produces erroneous shebangs. Fix them.
# https://bugzilla.redhat.com/show_bug.cgi?id=1335203
pathfix.py -i "%{__python3} %{py3_shbang_opts}u" -p -n %{buildroot}%{_bindir}/xonsh
pathfix.py -i "%{__python3} %{py3_shbang_opts}u" -p -n %{buildroot}%{_bindir}/xonsh-cat

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/lightdm/lightdm.conf.d
install -pm 0755 %{SOURCE2} %{buildroot}%{_sbindir}/
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/lightdm/lightdm.conf.d/

%check
# The tests only succeed if:
#
# - They are run from within a xonsh shell.
# - They are run with the `py.test-3` executable instead of `python3 -m pytest`.
#
# The run-tests.xsh script does those things for us.

sed --in-place "s:pytest:py.test-3:" run-tests.xsh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=%{buildroot}%{python3_sitelib} PATH="%{buildroot}%{_bindir}:$PATH" %{buildroot}%{_bindir}/xonsh run-tests.xsh

%post
if [ "$1" -ge 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    touch %{_sysconfdir}/shells
  fi
  for binpath in %{_bindir} /bin; do
    if ! grep -q "^${binpath}/xonsh$" %{_sysconfdir}/shells; then
       (cat %{_sysconfdir}/shells; echo "$binpath/xonsh") > %{_sysconfdir}/shells.new
       mv %{_sysconfdir}/shells{.new,}
    fi
  done
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -e '\!^%{_bindir}/xonsh$!d' -e '\!^/bin/xonsh$!d' < %{_sysconfdir}/shells > %{_sysconfdir}/shells.new
  mv %{_sysconfdir}/shells{.new,}
fi

%files
%doc README.rst
%license license
%{_bindir}/xonsh
%{_bindir}/xon.sh
%{_bindir}/xonsh-cat
%{python3_sitelib}/xonsh/
%{python3_sitelib}/xontrib/
%{python3_sitelib}/xonsh-%{version}*-py?.?.egg-info/
%{_datadir}/lightdm/lightdm.conf.d/65-xonsh.conf
%{_sbindir}/xonsh-session

%changelog
* Thu Jan 14 2020 Jerzy Drozdz <rpmbuilder@jdsieci.pl> - 0.9.13-3
- -l switch well behaviour
- exec implements all switches from bash/zsh

* Sun Jan 12 2020 Jerzy Drozdz <rpmbuilder@jdsieci.pl> - 0.9.13-2
- Added session wrapper script and related config

* Sun Jan 12 2020 Jerzy Drozdz <rpmbuilder@jdsieci.pl> - 0.9.13-1
- new version

* Thu Aug 29 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 0.9.11-1
- new version

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.10-3
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.10-2
- Rebuilt for Python 3.8

* Tue Aug 13 2019 Mairi Dulaney <jdulaney@fedoraproject.org> - 0.9.10-1
- Upgrade to latest release

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 0.9.6-1
- new version

* Sat May 18 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 0.9.3-1
- New upstream version

* Fri May 10 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 0.9.0-1
- New upstream version
- Python 3.4 support deprecated
- Tentative Python 3.8 support added

* Tue Apr 23 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 0.8.12-2
- Automatically add/remove xonsh to /etc/shells.

* Tue Apr 02 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 0.8.12-1
- New upstream release 0.8.12

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 John Dulaney <jdulaney@fedoraproject.org> - 0.6.9-1
- New upstream release

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.5-2
- Rebuilt for Python 3.7

* Thu May 31 2018 John Dulaney <jdulaney@fedoraproject.org> - 0.6.5-1
- New upstream release

* Sat Apr 14 2018 John Dulaney <jdulaney@fedoraproject.org> - 0.6.1-1
- New upstream release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.12-1
- New upstream release 0.5.12

* Mon May 29 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.10-1
- New upstream release 0.5.10

* Tue Apr 04 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.9-1
- New upstream release 0.5.9

* Sat Mar 11 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.8-1
- New upstream release 0.5.8

* Fri Mar 03 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.7-1
- New upstream release 0.5.7

* Fri Feb 24 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.6-1
- New upstream release 0.5.6

* Sun Feb 12 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.4-1
- New upstream release 0.5.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 07 2017 John Dulaney <jdulaney@fedoraproject.org> - 0.5.2-1
- New upstream release 0.5.2

* Sat Dec 24 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.5.1
- New upstream release 0.5.1

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.7-2
- Rebuild for Python 3.6

* Mon Oct 03 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.4.7-1
- New upstream release 0.4.7

* Sun Sep 04 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.4.6-1
- New upstream release 0.4.6

* Sun Aug 28 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.4.5-2
- Require python3-pygments and python3-setproctitle

* Sun Aug 28 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.4.5-1
- New upstream release 0.4.5

* Fri Aug  5 2016 Luke Macken <lmacken@redhat.com> - 0.4.4-2
- Require python3-prompt_toolkit to improve usability

* Thu Jul 21 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.4.4-1
- New upstream release 0.4.4

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 13 2016 John Dulaney <jdulaney@fedoraproject.org> - 0.4.3-1
- New upstream release 0.4.3

* Mon Jun 20 2016 Luke Macken <lmacken@redhat.com> - 0.3.4-1
- New upstream release 0.3.4

* Mon Jun 06 2016 Luke Macken <lmacken@redhat.com> - 0.3.3-1
- Latest upstream release
- Update the URL

* Fri Jun 03 2016 Luke Macken <lmacken@redhat.com> - 0.3.2-1
- Latest upstream release
- Update the Summary

* Mon Mar 16 2015 Robert Kuska <rkuska@redhat.com> - 0.1.2-1
- Initial package.
