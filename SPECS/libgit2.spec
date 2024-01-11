Name:           libgit2
Version:        0.26.8
Release:        2%{?dist}
Summary:        C implementation of the Git core methods as a library with a solid API
License:        GPLv2 with exceptions
URL:            http://libgit2.github.com/
Source0:        https://github.com/libgit2/libgit2/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        README.rhel8

Patch0001:      0001-Revert-cmake-disable-optimization-on-debug-builds.patch
Patch0002:      0002-CMakeLists-increase-strict-aliasing-level-to-3.patch
Patch0003:      0003-Disable-online-tests.patch
Patch0004:      0004-tests-Increase-TOOBIG-value-used-on-i686.patch
Patch0005:      0005-openssl-Use-the-system-profile-ciphers.patch

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  http-parser-devel
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  zlib-devel
Provides:       bundled(libxdiff)

%description
libgit2 is a portable, pure C implementation of the Git core methods 
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language
with bindings.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

# Remove VCS files from examples
find examples -name ".gitignore" -delete -print

# Fix pkgconfig generation
sed -i 's|@CMAKE_INSTALL_PREFIX@/||' libgit2.pc.in

# Remove bundled libraries
rm -frv deps

%build
mkdir %{_target_platform}
pushd %{_target_platform}
  %cmake -DTHREADSAFE=ON -DUSE_SSH=OFF ..
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}
mkdir -p %{buildroot}%{_docdir}/%{name}
install -p -m 0644 -t %{buildroot}%{_docdir}/%{name} %{SOURCE1}

%check
pushd %{_target_platform}
  ctest -VV
popd

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/%{name}.so.*

%files devel
%doc AUTHORS docs examples README.md
%doc %{_docdir}/%{name}/README.rhel8
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/git2.h
%{_includedir}/git2/

%changelog
* Tue Jun 02 2020 Brian C. Lane <bcl@redhat.com> - 0.26.8-2
- openssl: Use the system profile ciphers
  Resolves: rhbz#1842814

* Wed May 15 2019 Brian C. Lane <bcl@redhat.com> - 0.26.8-1
- Update to 0.26.8
  Resolves: rhbz#1638880
- Disable upstream online tests
  Related: rhbz#1638880
- tests: Increase TOOBIG value used on i686
  Related: rhbz#1638880

* Fri Sep 07 2018 Brian C. Lane <bcl@redhat.com> - 0.26.6-3
- CMakeLists increase strict aliasing level to 3
  Related: rhbz#1624129

* Wed Sep 05 2018 Brian C. Lane <bcl@redhat.com> - 0.26.6-2
- Revert overriding -O2 with -O0 in CMakeLists.txt
  Resolves: rhbz#1624129

* Mon Aug 27 2018 Brian C. Lane <bcl@redhat.com> - 0.26.6-1
- Update to 0.26.6 (CVE-2018-15501)
  Resolves: rhbz#1615588

* Mon Aug 13 2018 Brian C. Lane <bcl@redhat.com> - 0.26.5-2
- Use python3-devel in buildroot
  Resolves: rhbz#1615577

* Tue Jul 17 2018 Brian C. Lane <bcl@redhat.com> - 0.26.5-1
- Rebase to 0.26.5 (CVE-2018-11235, CVE-2018-10887, CVE-2018-10888)
- Disable SSH so that libssh2 is not required
- Use python3 when building
- Add README.rhel8 explaining why SSH is disabled

* Mon Mar 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26.3-1
- Update to 0.26.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26.0-4
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26.0-1
- Update to 0.26.0

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.25.1-3
- Backport patch to fix pkgconfig file under g-ir-scanner

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.25.1-2
- Bump release for rebuild

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.25.1-1
- Update to 0.25.1 (RHBZ #1395926)

* Tue Jan 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.24.6-1
- Update to 0.24.6 (RHBZ #1411857)

* Thu Nov 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.3-1
- Update to 0.24.3 (RHBZ #1391480)
- Add support for OpenSSL 1.1.0 (RHBZ #1383753)

* Mon Oct 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.2-2
- Backport patch for CVE-2016-8568, CVE-2016-8569

* Tue Oct 04 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.2-1
- Update to 0.24.2 (RHBZ #1381398)

* Wed Apr 13 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.24.1-1
- Update to 0.24.1

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.0-1
- Update to 0.24.0 (RHBZ #1310638)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.23.4-1
- Update to 0.23.4 (RHBZ #1281633)

* Tue Oct 06 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.23.3-1
- Update to 0.23.3 (RHBZ #1260324)

* Tue Sep 08 2015 Igor Gnatenko <ignatenko@src.gnome.org> - 0.23.2-1
- Update to 0.23.2

* Wed Sep 02 2015 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.23.1-1
- Update to 0.23.1
- Add curl support

* Thu Jul 30 2015 Igor Gnatenko <ignatenko@src.gnome.org> - 0.23.0-1
- Update to 0.23.0

* Fri Jul 03 2015 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.22.3-1
- Update to 0.22.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.22.2-1
- Update to 0.22.2

* Sat Feb 14 2015 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.22.1-1
- Update to 0.22.1

* Mon Jan 19 2015 Ignacio Casal Quinteiro <icq@gnome.org> - 0.22.0-1
- Update to 0.22.0

* Fri Dec 26 2014 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.21.3-1
- Update to 0.21.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Christopher Meng <rpm@cicku.me> - 0.21.1-1
- Update to 0.21.1

* Fri Jul 18 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.21.0-2
- Fix memory alignment issues on arm, aarch64, ppc64le (#1115905)

* Sat Jun 21 2014 Christopher Meng <rpm@cicku.me> - 0.21.0-1
- Update to 0.21.0

* Fri Jun 06 2014 Karsten Hopp <karsten@redhat.com> 0.20.0-4
- temporarily disable checks on ppc64 and s390x (Bugzilla 1105552)

* Thu Mar 27 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 0.20.0-3
- Fix build requirement on libssh2-devel. (RHBZ#1039433)

* Tue Mar 25 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 0.20.0-2
- Build with the bundled xdiff.
- Disable a failing test. (libgit2#2199)
- Add missing build requirement on libssh2. (RHBZ#1039433)
- Build a thread-safe libgit2.

* Sun Nov 24 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 0.20.0-1
- 0.20.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.19.0-1
- 0.19.0

* Wed Jun 19 2013 Dan Horák <dan[at]danny.cz> - 0.18.0-5
- Add htonl() and friends declarations on non-x86 arches
- Rebuilt with fixed libxdiff for big endian arches

* Thu May 30 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.18.0-4
- Update the http-parser patch
- Skip tests that require network connectivity

* Thu May 30 2013 Tom Callaway <spot@fedoraproject.org> - 0.18.0-3
- use system libxdiff instead of bundled copy

* Fri May 24 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.18.0-2
- Remove unnecessary CMake build flags
- Fix the pkgconfig file

* Thu May 02 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.18.0-1
- Update to version 0.18.0
- Unbundle the http-parser library

* Fri Oct 19 2012 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.17.0-2
- Use make for building and installation
- Specify minimum CMake version
- Remove useless OpenSSL build dependency
- Move development documentation to the -devel package
- Add code examples to the -devel package

* Thu Oct 18 2012 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.17.0-1
- Initial package.
