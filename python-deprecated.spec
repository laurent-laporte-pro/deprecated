%global srcname Deprecated
%global pkgname deprecated

Name:           python-%{pkgname}
Version:        1.3.1
Release:        1%{?dist}
Summary:        Python decorator to deprecate old python classes, functions or methods
License:        MIT
URL:            https://github.com/laurent-laporte-pro/%{pkgname}
Source0:        %{pypi_source %{pkgname}}
BuildArch:      noarch

%description
Python @deprecated decorator to deprecate old python classes,
functions or methods.

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{pkgname}
Python @deprecated decorator to deprecate old python classes,
functions or methods.

%prep
%autosetup -n %{pkgname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pkgname}

%check
%pyproject_check_import

%files -n python3-%{pkgname} -f %{pyproject_files}
%license LICENSE.rst
%doc README.md


%changelog
* Fri Jul 26 2019 Petr Hracek <phracek@redhat.com> - 1.2.6-2
- Fix python3_sitelib issue

* Fri Jul 26 2019 Petr Hracek <phracek@redhat.com> - 1.2.6-1
- Initial package
