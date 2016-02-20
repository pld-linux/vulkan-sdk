#
# Conditional build:
%bcond_with	tests		# build with tests (require a working Vulkan
				# driver (ICD))
#
%define	tag	windows-rt-%{version}
Summary:	Vulkan API loader
Name:		vulkan-loader
Version:	1.0.3.0
Release:	3
License:	MIT-like
Group:		Applications
Source0:	https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers/archive/%{tag}/%{name}-%{version}.tar.gz
# Source0-md5:	0691d2d79cf62902df2973bbdf594028
Patch0:		system_glslang.patch
URL:		https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers
#BuildRequires:	LunarGLASS-devel
BuildRequires:	cmake
BuildRequires:	glslang
BuildRequires:	glslang-devel
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	spirv-tools-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common loader for Vulkan API drivers.

%package -n vulkan-layers
Summary:	Validation layers for Vulkan
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n vulkan-layers
Validation layers for Vulkan.

%package -n vulkan-devel
Summary:	Header files for the Vulkan API
Summary(pl.UTF-8):	Pliki nagłówkowe API Vulkan
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n vulkan-devel
Header files for the Vulkan API.

%description -n vulkan-devel -l pl.UTF-8
Pliki nagłówkowe API Vulkan.

%package demos
Summary:	Vulkan demos
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description demos
Vulkan demos.

%package utils
Summary:	Vulkan loader utilities
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description utils
Vulkan loader utilities.

%prep
%setup -qn Vulkan-LoaderAndValidationLayers-%{tag}
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_DATADIR=share \
	-DCMAKE_INSTALL_SYSCONFDIR=etc \
	%{?with_tests:-DBUILD_TESTS=ON} \
	%{!?with_tests:-DBUILD_TESTS=OFF} \
		../
%{__make}

%if %{with tests}
cd tests
LC_ALL=C.utf-8 VK_LAYER_PATH=../layers LD_LIBRARY_PATH=../loader:../layers ./run_all_tests.sh
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/icd.d \
$RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/{explicit,implicit}_layer.d \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/vulkan/layer} \
	$RPM_BUILD_ROOT%{_includedir}/vulkan \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}


cd build
%{__make} install

cp -p loader/libvulkan.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}
ln -s libvulkan.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}/libvulkan.so
ln -s libvulkan.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}/libvulkan.so.1

cp -p demos/vulkaninfo $RPM_BUILD_ROOT%{_bindir}/vulkaninfo
cp -p demos/tri $RPM_BUILD_ROOT%{_bindir}/vulkan-tri
cp -p demos/cube $RPM_BUILD_ROOT%{_bindir}/vulkan-cube

cp -p install_staging/*.so $RPM_BUILD_ROOT%{_libdir}/vulkan/layer
for f in layers/*.json ; do
sed -e's@"library_path": "./@"library_path": "%{_libdir}/vulkan/layer/@' $f > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/$(basename $f)
done

cp -p libs/vkjson/libvkjson.a $RPM_BUILD_ROOT%{_libdir}
cp -p libs/vkjson/vkjson_{info,unittest} $RPM_BUILD_ROOT%{_bindir}

cd ..

cp -p libs/vkjson/vkjson.h $RPM_BUILD_ROOT%{_includedir}
cp -p include/vulkan/* $RPM_BUILD_ROOT%{_includedir}/vulkan

cp -p demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%doc loader/{README.md,LoaderAndLayerInterface.md,LinuxICDs.txt}
%dir %{_sysconfdir}/vulkan
%dir %{_sysconfdir}/vulkan/icd.d
%dir %{_sysconfdir}/vulkan/explicit_layer.d
%dir %{_sysconfdir}/vulkan/implicit_layer.d
%dir %{_datadir}/vulkan
%dir %{_datadir}/vulkan/icd.d
%dir %{_datadir}/vulkan/explicit_layer.d
%dir %{_datadir}/vulkan/implicit_layer.d
%{_libdir}/libvulkan.so.1.*.*
%ghost %{_libdir}/libvulkan.so.1
%dir %{_libdir}/vulkan

%files demos
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vulkan-tri
%attr(755,root,root) %{_bindir}/vulkan-cube

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vulkaninfo
%attr(755,root,root) %{_bindir}/vkjson_info
%attr(755,root,root) %{_bindir}/vkjson_unittest

%files -n vulkan-layers
%defattr(644,root,root,755)
%doc LICENSE.txt layers/README.md layers/vk_layer_settings.txt
%dir %{_libdir}/vulkan/layer
%{_libdir}/vulkan/layer/*.so
%{_datadir}/vulkan/explicit_layer.d/*.json

%files -n vulkan-devel
%defattr(644,root,root,755)
%doc LICENSE.txt README.md
%{_libdir}/libvulkan.so
%{_libdir}/libvkjson.a
%{_includedir}/vulkan
%{_includedir}/vkjson.h
%{_examplesdir}/%{name}-%{version}
