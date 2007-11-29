Summary:	ELILO: EFI Linux Boot Loader
Summary(pl.UTF-8):	ELILO - linuksowy bootloader dla platform EFI
Name:		elilo
Version:	3.7
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://dl.sourceforge.net/elilo/%{name}-%{version}.tar.gz
# Source0-md5:	980311f59f7c7ab1aa2a77f74db825d0
URL:		http://elilo.sourceforge.net/
BuildRequires:	gnu-efi >= 3.0d
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ELILO is the EFI Linux boot loader for IA-64 (IPF), IA-32 (x86) and
x86_64 EFI-based platforms.

%description -l pl.UTF-8
ELILO to linuksowy bootloader dla platform IA-64 (IPF), IA-32 (x86)
oraz x86_64 opartych na EFI.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	OPTIMFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/boot/efi}

install tools/eliloalt $RPM_BUILD_ROOT%{_sbindir}
install elilo.efi $RPM_BUILD_ROOT/boot/efi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README* TODO docs/*.txt examples
%attr(755,root,root) %{_sbindir}/eliloalt
%dir /boot/efi
/boot/efi/elilo.efi
