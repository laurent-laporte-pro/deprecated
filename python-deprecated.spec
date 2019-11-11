%global srcname Deprecated
%global pkgname deprecated

Name:           python-%{pkgname}
Version:        1.2.8
Release:        2%{?dist}
Summary:        Python decorator to deprecate old python classes, functions or methods
License:        MIT
URL:            https://github.com/tantale/%{pkgname}
Source0:        https://files.pythonhosted.org/packages/source/D/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description
Python @deprecated decorator to deprecate old python classes,
functions or methods.

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
Python @deprecated decorator to deprecate old python classes,
functions or methods.

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{pkgname}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkgname}
%license LICENSE.rst
%doc README.md
%{python3_sitelib}/%{pkgname}/
%{python3_sitelib}/%{srcname}-%{version}-*.egg-info/


%changelog
* Fri Jul 26 2019 Petr Hracek <phracek@redhat.com> - 1.2.8-2
- Fix python3_sitelib issue

* Fri Jul 26 2019 Petr Hracek <phracek@redhat.com> - 1.2.8-1
- Initial package
