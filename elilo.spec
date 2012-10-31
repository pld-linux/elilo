Summary:	ELILO: EFI Linux Boot Loader
Summary(pl.UTF-8):	ELILO - linuksowy bootloader dla platform EFI
Name:		elilo
Version:	3.14
Release:	1.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/elilo/%{name}-%{version}-all.tar.gz
# Source0-md5:	d16086bcb228d2c25e241d73c1bf36be
Source1:	%{name}.conf
Source2:	%{name}.efi-boot-update
URL:		http://elilo.sourceforge.net/
BuildRequires:	gnu-efi >= 3.0d
Suggests:	efi-boot-update
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define	efi_arch ia32
%endif
%ifarch %{x8664}
%define	efi_arch x64
%endif
%ifarch ia64
%define	efi_arch ia64
%endif

%description
ELILO is the EFI Linux boot loader for IA-64 (IPF), IA-32 (x86) and
x86_64 EFI-based platforms.

%description -l pl.UTF-8
ELILO to linuksowy bootloader dla platform IA-64 (IPF), IA-32 (x86)
oraz x86_64 opartych na EFI.

%prep
%setup -q -c

tar xf elilo-%{version}-source.tar.gz

%build
%{__make} -C elilo -j1 \
	ARCH=$(echo %{_target_base_arch} | sed -e 's/i386/ia32/') \
	CC="%{__cc}" \
	OPTIMFLAGS="%{rpmcflags}" \
	EFICRT0=%{_libdir} \
	EFILIB=%{_libdir} \
	GNUEFILIB=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/lib/efi/%{efi_arch}} \
		$RPM_BUILD_ROOT/etc/efi-boot/update.d

install elilo/tools/eliloalt $RPM_BUILD_ROOT%{_sbindir}
install elilo/elilo.efi $RPM_BUILD_ROOT/lib/efi/%{efi_arch}/elilo.efi

install %{SOURCE1}  $RPM_BUILD_ROOT/etc/efi-boot/%{name}.conf
sed -e's/ARCH=.*/ARCH=%{efi_arch}/' %{SOURCE2} \
		> $RPM_BUILD_ROOT/etc/efi-boot/update.d/%{name}.conf

%triggerpostun -- %{name} < 3.14-1.1
# someone may have boot configured from this misplaced location
# better put elilo.efi copy there too
echo "Upgrade detected, copying elilo.efi to /boot/efi/elilo.efi..."
cp --preserve=ship,timestamps /lib/efi/%{efi_arch}/elilo.efi /boot/efi/elilo.efi || :
echo "Remove /boot/efi/elilo.efi if you don't need it."

%post
/sbin/efi-boot-update --auto || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{version}-release-notes.txt elilo/{ChangeLog,README*,TODO} elilo/docs/*.txt elilo/examples
%attr(755,root,root) %{_sbindir}/eliloalt
/etc/efi-boot/%{name}.conf
/etc/efi-boot/update.d/%{name}.conf
/lib/efi/%{efi_arch}/elilo.efi
