# find the HornetQ version from the tarball
%define hornetq_url %((grep hornetq %{_sourcedir}/sources || \
                        grep hornetq %{_builddir}/sources  || \
                        echo "x unknown") 2>/dev/null | perl -ane 'print("$F[1]")')
%define hornetq_tar %(basename %{hornetq_url})
%define hornetq_version %(echo %{hornetq_tar} | perl -pe 's/^hornetq-//; s/\\.tar\\.gz$//')

# installation settings
%define hornetq_share /usr/share/hornetq
%define hornetq_home  /usr/share/hornetq-%{hornetq_version}

Summary:	HornetQ Messaging Broker
Name:		mig-hornetq
Version:	%{hornetq_version}
Release:	1%{?dist}
License:	Apache v2.0
Group:		System
Source0:	%{hornetq_tar}
Source1:	hornetq.init
Source2:	sources
URL: 		http://www.jboss.org/hornetq
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	perl
BuildArch:	noarch

%description
HornetQ is an open source project to build a multi-protocol, embeddable,
very high performance, clustered, asynchronous messaging system.

%prep
%setup -q -n hornetq-%{hornetq_version}

%build
# add our service script
install -m 0755 %{SOURCE1} bin/service

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{hornetq_home}/libaio
mv bin/libHornetQAIO*.so %{buildroot}%{hornetq_home}/libaio
mv * %{buildroot}%{hornetq_home}

%post
[ -e %{hornetq_share} ] && rm -f %{hornetq_share}
ln -s hornetq-%{hornetq_version} %{hornetq_share}

%postun
rm -f %{hornetq_share}
cd /usr/share
last=`ls -d hornetq-* 2>/dev/null | sort | tail -1`
if [ "x$last" != "x" ]; then
  ln -s $last %{hornetq_share}
fi

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%{hornetq_home}
