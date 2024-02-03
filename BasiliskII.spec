%global commit e273bb1a0b4f6e35bcdbf6cf918aa0ca3e6d99da
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define date 20171001

Summary:        68k Macintosh emulator
Name:           BasiliskII
Version:        1.0
Release:        0.%{date}.7%{?dist}.12
License:        GPLv2+
URL:            http://basilisk.cebix.net/
Source0:        https://github.com/cebix/macemu/archive/%{commit}/BasiliskII-1.0-%{shortcommit}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.png
Source3:        %{name}.appdata.xml
# For some reason AC_PATH_XTRA does not work on the rpmfusion buildsys ?
# I've tried reproducing this with mock on both x86_64 and arm, without success
Patch1:         macemu-work-around-ac_path_xtra-not-working.patch
# Patch 10+ because these are for cxmon
Patch10:        cxmon-3.2-hide-symbols.patch
Patch11:        cxmon-3.2-strfmt.patch
Patch12:        cxmon-3.2-fpermissive.patch
BuildRequires:  libtool gcc-c++ gtk2-devel
BuildRequires:  desktop-file-utils libappstream-glib readline-devel
BuildRequires:  libXt-devel libXxf86vm-devel SDL-devel
Requires:       hicolor-icon-theme

%description
Basilisk II is an Open Source 68k Macintosh emulator. That is, it enables
you to run 68k MacOS software on you computer, even if you are using a
different operating system. However, you still need a copy of MacOS and
a Macintosh ROM image to use Basilisk II.


%prep
%autosetup -p1 -n macemu-%{commit}
# cleanup
iconv -f ISO_8859-1 -t UTF8 %{name}/README > README
touch -r %{name}/README README
iconv -f ISO_8859-1 -t UTF8 %{name}/ChangeLog > ChangeLog
touch -r ChangeLog %{name}/ChangeLog
sed -i 's/\r//' %{name}/src/Unix/tinyxml2.cpp
chmod -x %{name}/src/Unix/tinyxml2.cpp %{name}/src/Unix/tinyxml2.h
# autogen
pushd %{name}/src/Unix
NO_CONFIGURE=1 ./autogen.sh
popd


%build
pushd %{name}/src/Unix
mkdir obj
%configure --datadir=%{_sysconfdir} \
    --disable-xf86-dga --enable-sdl-audio --with-bincue
make %{?_smp_mflags}
popd


%install
pushd %{name}/src/Unix
%make_install
popd
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tunconfig

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}

install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

install -D -p -m 0644 %{SOURCE3} \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc ChangeLog README %{name}/TECH %{name}/TODO
%license %{name}/COPYING
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/fbdevices
%config(noreplace) %{_sysconfdir}/%{name}/keycodes
%{_sysconfdir}/%{name}/tunconfig
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_mandir}/man1/%{name}.1*


%changelog
* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0-0.20171001.7.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0-0.20171001.7.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0-0.20171001.7.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Tue Feb 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0-0.20171001.7.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Feb 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0-0.20171001.7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0-0.20171001.7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct  1 2017 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0-0.20171001.7
- BasiliskII git snapshot du-jour
- Fix FTBFS on F27+

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0-0.20160322.6.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0-0.20160322.6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 22 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0-0.20160322.6
- BasiliskII git snapshot du-jour
- Use proper github download URL
- New version comes with bundled cxmon
- Add appdata
- Add a workaround for FTBFS weirdness in rpmfusion buildsys (rf#3633)

* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0-0.20150516.5
- BasiliskII git snapshot du-jour
- Fix FTBFS (rf#3633)

* Sat Aug 30 2014 Sérgio Basto <sergio@serjux.com> - 1.0-0.20130310.4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0-0.20130310.4
- New upstream: http://basilisk.cebix.net/
- Uses github, no source tarbals :| Update to todays git master (bbc0af47)
- Modernize spec
- Fix FTBFS (since F-11 !)
- Switch from esound (deprecated / obsolete) to SDL for sound output

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.20060501.3.4
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.20060501.3.3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.20060501.3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0-0.20060501.3.1
- rebuild for new F11 features

* Sat Oct 18 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 1.0-0.20060501.3
- Updated release of cxmon to 3.2
- Fix compilation with latest stdlibc++
- Regenerate Patch0, nuke _default_patch_fuzz 2
- Fixup desktop file Categories, so that Basilisk will show up under the
  Emulators menu where it belongs
- Make rpmlint like this package

* Sat Oct 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.0-0.20060501.2
- rebuild for RPM Fusion
- _default_patch_fuzz 2
- remove support for building against XFree86

* Wed Mar  7 2007 Matthias Saou <http://freshrpms.net/> 1.0-0.20060501.1
- Update to 01052006.
- Update URL and source locations.

* Wed Mar 22 2006 Matthias Saou <http://freshrpms.net/> 1.0-0.20051122.5
- Add missing modular X build requirements.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 1.0-0.20051122.4
- Release bump to drop the disttag number in FC5 build.

* Thu Jan 12 2006 Matthias Saou <http://freshrpms.net/> 1.0-0.20051122.3
- Add modular xorg build switch, and make it the default.

* Thu Dec  1 2005 Matthias Saou <http://freshrpms.net/> 1.0-0.20051122
- Update to 20051122 snapshot.
- Add --with sdl rebuild option.
- Switch from gtk1 to new gtk2 GUI.

* Fri Apr  1 2005 Matthias Saou <http://freshrpms.net/> 1.0-0.20050322
- Update to latest snapshot.
- Add a menu entry.
- Addressing of "banks" type is still required.
- SDL still doesn't display properly.
- Add cxmon support, can be disabled with --without mon.
- Add readline-devel build dependency.
- Disable binary stripping on make install to get a useful debuginfo package.

* Mon Dec 13 2004 Matthias Saou <http://freshrpms.net/> 1.0-0.20041109
- Update to latest BasilikII JIT snapshot.
- Override datadir to sysconfdir as it makes more sense to have configuration
  files there.
- Force addressing to older "banks" on FC3 as other don't work :-(

* Sat Feb 15 2003 Dag Wieers <dag@wieers.com> - 0.9.20020115-0
- Initial package. (using DAR)

