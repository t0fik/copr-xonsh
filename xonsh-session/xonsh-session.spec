Name:           xonsh-session
Version:        1.0.0
Release:        1%{?dist}
Summary:        Provides session configuration for xonsh shell

License:        GPL
URL:            https://github.com/t0fik/copr-xonsh
Source0:        xonsh-session
Source1:        65-xonsh.conf

Requires:       xonsh
Supplements:    xonsh

%description
Provides graphical session configuration for xonsh shell
%prep
%build

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/lightdm/lightdm.conf.d
install -pm 0755 %{SOURCE0} %{buildroot}%{_sbindir}/
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/lightdm/lightdm.conf.d/

%files
%license
%{_datadir}/lightdm/lightdm.conf.d/65-xonsh.conf
%{_sbindir}/xonsh-session


%changelog
* Sun Nov 07 2021 Jerzy Drozdz <jerzy.drozdz@jdsieci.pl> - 1.0.0-1
- Initial build

