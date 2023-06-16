%define debug_package %{nil}

%global _dwz_low_mem_die_limit 0

%global provider        github
%global provider_tld	com
%global project         shatteredsilicon
%global repo            rds_exporter
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}

Name:		%{repo}
Version:	%{_version}
Release:	%{_release}
Summary:	Prometheus exporter for RDS metrics, written in Go with pluggable metric collectors

License:	ASL 2.0
URL:		https://%{provider_prefix}
Source0:	%{repo}-%{version}.tar.gz

BuildRequires:	golang

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
rds_exporter is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -n %{name}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}


%build
export GOPATH=$(pwd)
mkdir -p vendor/github.com/cespare/xxhash/v2
find vendor/github.com/cespare/xxhash  ! -path '*/v2' -mindepth 1 -maxdepth 1 -exec mv {} vendor/github.com/cespare/xxhash/v2 \;
GO111MODULE=off go install -ldflags "${LDFLAGS:-} -s -w -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -a -v -x %{provider_prefix}


%install
install -d -p %{buildroot}%{_sbindir}
install -p -m 0755 ./bin/%{repo} %{buildroot}%{_sbindir}/%{repo}


%files
%license src/%{provider_prefix}/LICENSE
%doc src/%{provider_prefix}/README.md
%{_sbindir}/%{name}


%changelog
* Thu Nov 16 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.5.0-1
- move repository from Percona-Lab to percona organization
