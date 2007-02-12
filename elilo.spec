Summary:	ELILO: EFI Linux Boot Loader
Summary(pl.UTF-8):   ELILO - linuksowy bootloader dla platform EFI
Name:		elilo
Version:	3.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/elilo/%{name}-%{version}.tgz
# Source0-md5:	5fa5d3d1ac2f29e3b56a4e82b752ecd6
URL:		http://elilo.sourceforge.net/
BuildRequires:	gnu-efi >= 3.0a
ExclusiveArch:	%{ix86} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ELILO is the EFI Linux boot loader for IA-64 (IPF) and IA-32 (x86)
EFI-based platforms.

%description -l pl.UTF-8
ELILO to linuksowy bootloader dla platform IA-64 (IPF) i IA-32 (x86)
opartych na EFI.

%prep
%setup -q -n %{name}

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
