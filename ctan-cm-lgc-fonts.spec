%define foundryname  ctan
%define fontpkg      cm-lgc
%define fontname     %{foundryname}-%{fontpkg}
%define fontconf     64-%{fontname}
%define ctan_date    20051007
%define texfonts     %{_texmf_main}/fonts
%define texfontpath  public/%{fontpkg}


# Common description
%define common_desc The CM-LGC PostScript Type 1 fonts are converted from the METAFONT \
sources of the Computer Modern font families. CM-LGC supports the T1, T2A, \
LGR, and TS1 encodings, i.e. Latin, Cyrillic, and Greek.


Name:           ctan-cm-lgc-fonts
Version:        0.5
Release:        17.1%{?dist}
Summary:        CM-LGC Type1 fonts
Group:          Applications/Publishing
# Font exception
License:        GPLv2+ with exceptions
URL:            http://www.ctan.org/tex-archive/fonts/ps-type1/cm-lgc
Source0:        cm-lgc-%{ctan_date}.zip
# upstream source - unversioned zip file
# ftp://tug.ctan.org/pub/tex-archive/fonts/ps-type1/cm-lgc.zip
Source1:        %{fontname}-fontconfig.tar.gz
# Tarball of fontconfig files for each font
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  fontpackages-devel, texlive-texmf
BuildArch:      noarch
%description
%{common_desc} 


%package common
Summary:  CM-LGC Type 1 fonts, common files (documentation…)
Group:    User Interface/X
Requires: fontpackages-filesystem
%description common
%common_desc
This package consists of files used by other ctan-cm-lgc-fonts packages.


%define romanfonts %{fontname}-roman-fonts
%package -n %{romanfonts}
Summary:   CM-LGC Type 1 fonts, serif font faces
Group:     User Interface/X
Requires:  %{name}-common = %{version}-%{release}
%description -n %{romanfonts}
%common_desc
This package contains the CM-LGC serif typeface based on Computer Modern.

%_font_pkg -n roman -f %{fontconf}-roman.conf fcm*


%define sansfonts %{fontname}-sans-fonts
%package -n %{sansfonts}
Summary:   CM-LGC Type 1 fonts, sans-serif font faces
Group:     User Interface/X
Requires:  %{name}-common = %{version}-%{release}
%description -n %{sansfonts}
%common_desc
This package contains the CM-LGC sans-serif typeface based on Computer Modern.

%_font_pkg -n sans -f %{fontconf}-sans.conf fcs*


%define typewriterfonts %{fontname}-typewriter-fonts
%package -n %{typewriterfonts}
Summary:   CM-LGC Type 1 fonts, typewriter font faces
Group:     User Interface/X
Requires:  %{name}-common = %{version}-%{release}
%description -n %{typewriterfonts}
%common_desc
This package contains the CM-LGC serif typeface based on Computer Modern.

%_font_pkg -n typewriter -f %{fontconf}-typewriter.conf fct*


%define texfontpkg tex-cm-lgc
%package -n %{texfontpkg}
Summary:  CM-LGC Type1 fonts, TeX support files
Group:    User Interface/X
Requires: %{romanfonts} = %{version}-%{release}, %{sansfonts} = %{version}-%{release}, %{typewriterfonts} = %{version}-%{release}
Requires: tex(latex)
Provides: tetex-font-cm-lgc = %{version}-%{release}
Obsoletes: tetex-font-cm-lgc < 0.5-12
%description -n %{texfontpkg}
%{common_desc}
TeX support files.


%prep
%setup -q -a1 -n %{fontpkg}


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_texmf_main}/tex/latex/%{fontpkg}
mkdir -p %{buildroot}%{texfonts}/{afm,ofm,ovf,type1,tfm,vf}/%{texfontpath}
mkdir -p %{buildroot}%{texfonts}/{enc,map}/dvips/%{fontpkg}

install -m 644 -p tex/latex/%{fontpkg}/* %{buildroot}%{_texmf_main}/tex/latex/%{fontpkg}/
install -m 644 -p fonts/ofm/%{texfontpath}/* %{buildroot}%{texfonts}/ofm/%{texfontpath}/
install -m 644 -p fonts/ovf/%{texfontpath}/* %{buildroot}%{texfonts}/ovf/%{texfontpath}/
install -m 644 -p fonts/tfm/%{texfontpath}/* %{buildroot}%{texfonts}/tfm/%{texfontpath}/
install -m 644 -p fonts/vf/%{texfontpath}/* %{buildroot}%{texfonts}/vf/%{texfontpath}/
install -m 644 -p dvips/base/* %{buildroot}%{texfonts}/enc/dvips/%{fontpkg}/
install -m 644 -p dvips/config/* %{buildroot}%{texfonts}/map/dvips/%{fontpkg}/

#install .pfb and .afm files in %{_fontdir} as per the fedora font guidelines
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p fonts/type1/%{texfontpath}/* %{buildroot}%{_fontdir}
install -m 0644 -p fonts/afm/%{texfontpath}/* %{buildroot}%{_fontdir}

pushd %{buildroot}%{_fontdir}
for pfb_file in *.pfb ;  do
    ln -s %{_fontdir}/$pfb_file %{buildroot}%{texfonts}/type1/%{texfontpath}/$pfb_file
done
for afm_file in *.afm ;  do
    ln -s %{_fontdir}/$afm_file %{buildroot}%{texfonts}/afm/%{texfontpath}/$afm_file
done
popd


# fontconfig stuff (see spectemplate-fonts-multi.spec)
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p fontconfig/%{fontname}-roman.conf \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-roman.conf
install -m 0644 -p fontconfig/%{fontname}-sans.conf \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p fontconfig/%{fontname}-typewriter.conf \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-typewriter.conf

for fconf in %{fontconf}-roman.conf \
             %{fontconf}-sans.conf \
             %{fontconf}-typewriter.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done



%clean
rm -rf %{buildroot}


%post -n %{texfontpkg}
texhash
conffile="$(texconfig-sys conf | grep updmap.cfg)"
if [ "$1" -eq "1" ]; then
    updmap-sys --quiet --nohash --cnffile ${conffile} --enable Map %{fontpkg}.map
fi



%postun -n %{texfontpkg}
conffile="$(texconfig-sys conf | grep updmap.cfg)"
if [ "$1" -eq "0" ]; then
  updmap-sys --quiet --nohash --cnffile ${conffile} --disable %{fontpkg}.map
fi
texhash



%files common
%defattr(0644,root,root,0755)
%doc COPYING HISTORY README
%dir %{_fontdir}


%files -n %{texfontpkg}
%defattr(0644,root,root,0755)
%{_texmf_main}/tex/latex/%{fontpkg}
%{texfonts}/afm/%{texfontpath}
%{texfonts}/ofm/%{texfontpath}
%{texfonts}/ovf/%{texfontpath}
%{texfonts}/tfm/%{texfontpath}
%{texfonts}/type1/%{texfontpath}
%{texfonts}/vf/%{texfontpath}
%{texfonts}/enc/dvips/%{fontpkg}
%{texfonts}/map/dvips/%{fontpkg}



%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.5-17.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-15
- Address comments in https://bugzilla.redhat.com/show_bug.cgi?id=480589#c2
  (thanks Nicolas Mailhot)
    - Add a buildrequires for texlive-texmf
    - Remove Requires: fontpackages-filesystem from main and add to common
      subpackage.

* Fri Jan 16 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-14
- Rename the package to ctan-cm-lgc-fonts
- Name the subpackages according to 
  http://fedoraproject.org/wiki/PackagingDrafts/Font_package_naming_(2009-01-13)
- Update to fontpackages-* >= 1.15

* Tue Jan 13 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-13
- Divide font families into subpackages (roman, sans, typewriter)

* Mon Jan 12 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-12
- Minor package description enhancement.
- Explicit vr Requires to the subpackage.

* Mon Jan 12 2009 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-11
- Restructure spec file according to
  https://fedoraproject.org/wiki/Fonts_SIG_Fedora_11_packaging_changes
  (bug #477461)
- Split package to cm-lgc-fonts (.pfb and .afm) and tetex-font-cm-lgc 
  (TeX stuff)
- Include .afm files (forgotten in the previous versions)

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5-10
- fix license tag

* Fri Jan  4 2008 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-9
- Drop -fonts requires.

* Tue Aug 29 2006 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-8
- Bump release for FC6 rebuild.

* Mon Feb 20 2006 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-6
- Rebuild for FC5.

* Sun Nov  6 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-6
- Use run-time define updmap.cfg (Michal Jaegermann, bug #172491).

* Wed Nov  2 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-5
- Use absolute path commands in post and postun.

* Wed Nov  2 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-4
- Remove explicit outputdir for updmap-sys (bug #172268)
- Readd texhash in post and postun.

* Fri Oct  7 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-3
- Require tetex-fonts.
- Drop cm-lgc-test.tex.
- Use ctan zip soure.
- Other cleanups.

* Wed Jul  6 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-2
- Run updmap-sys only when installing, not when updating

* Wed Jun 15 2005 Sarantis Paskalis <paskalis@di.uoa.gr> - 0.5-1
- update to 0.5 (#160464)
- make the package tetex-3 compliant (use updmap-sys instead of updmap,
  update location for .enc and .map files).

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Nov 28 2004 Michael Schwendt <mschwendt[AT]users.sf.net>
- Make tarball file name unique.

* Sun Oct 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.3.1-1
- Updated to 0.3.1.

* Sat Jun  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.3-0.fdr.1
- Updated to 0.3.

* Wed May  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.2.1-0.fdr.2
- Removed INSTALL file (bug 997).
- Added cm-lgc-test.tex test document (bug 997).
- Moved preun script to postun (bug 997).
- Split Requires(post,postun) into separate Require statements (bug 997).

* Sun Nov 16 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.2.1-0.fdr.1
- Initial Fedora RPM release.
