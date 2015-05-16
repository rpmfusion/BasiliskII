%define date 20150516
%define mon_version 3.2

Summary:        68k Macintosh emulator
Name:           BasiliskII
Version:        1.0
Release:        0.%{date}.5%{?dist}
License:        GPLv2+
URL:            http://basilisk.cebix.net/
# GRRR github, no url ...
Source0:        macemu-master.zip
Source1:        cxmon-3.2-cvs20130310.tar.gz
Source2:        BasiliskII.png
# Patch 10+ because this is for Source1 rather then Source0
Patch10:        cxmon-3.2-hide-symbols.patch
Patch11:        cxmon-3.2-strfmt.patch
BuildRequires:  libtool gcc-c++ gtk2-devel
BuildRequires:  desktop-file-utils readline-devel
BuildRequires:  libXt-devel libXxf86vm-devel SDL-devel
Requires:       hicolor-icon-theme

%description
Basilisk II is an Open Source 68k Macintosh emulator. That is, it enables
you to run 68k MacOS software on you computer, even if you are using a
different operating system. However, you still need a copy of MacOS and
a Macintosh ROM image to use Basilisk II.


%prep
%setup -q -a 1 -n macemu-master
pushd cxmon-%{mon_version}
%patch10 -p1
%patch11 -p1
popd
iconv -f ISO_8859-1 -t UTF8 BasiliskII/README > README
touch -r BasiliskII/README README
iconv -f ISO_8859-1 -t UTF8 BasiliskII/ChangeLog > ChangeLog
touch -r ChangeLog BasiliskII/ChangeLog


%build
pushd BasiliskII/src/Unix
NO_CONFIGURE=1 ./autogen.sh
%configure --datadir=%{_sysconfdir} \
    --with-mon=../../../cxmon-%{mon_version}/src \
    --disable-xf86-dga --enable-sdl-audio --with-bincue
make %{?_smp_mflags}
popd


%install
pushd BasiliskII/src/Unix
%make_install
popd
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tunconfig

# Create the system menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Basilisk II
Comment=68k Macintosh Emulator
Exec=BasiliskII
Icon=BasiliskII
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
%if 0%{?fedora} && 0%{?fedora} < 19
    --vendor rpmforge \
%endif
    %{name}.desktop

install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/BasiliskII.png


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
%doc ChangeLog README BasiliskII/COPYING BasiliskII/TECH BasiliskII/TODO
%dir %{_sysconfdir}/BasiliskII/
%config(noreplace) %{_sysconfdir}/BasiliskII/fbdevices
%config(noreplace) %{_sysconfdir}/BasiliskII/keycodes
%{_sysconfdir}/BasiliskII/tunconfig
%{_bindir}/BasiliskII
%{_datadir}/icons/hicolor/32x32/apps/BasiliskII.png
%{_datadir}/applications/*%{name}.desktop
%{_mandir}/man1/BasiliskII.1*


%changelog
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

