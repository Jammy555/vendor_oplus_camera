# Blob dependencies
PRODUCT_PACKAGES += \
    android.hardware.graphics.common-V3-ndk.vendor

# Init
PRODUCT_PACKAGES += \
    init.oplus.camera.rc

# Permissions
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/permissions/oplus_google_lens_config.xml:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/permissions/oplus_google_lens_config.xml \
    $(LOCAL_PATH)/configs/permissions/privapp-permissions-oplus.xml:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/permissions/privapp-permissions-oplus.xml \
    $(LOCAL_PATH)/configs/permissions/oplus.feature.android.xml:$(TARGET_COPY_OUT_PRODUCT)/etc/permissions/oplus.feature.android.xml \
    $(LOCAL_PATH)/configs/sysconfig/hiddenapi-package-oplus-whitelist.xml:$(TARGET_COPY_OUT_SYSTEM)/etc/sysconfig/hiddenapi-package-oplus-whitelist.xml

# System Ext Camera Properties
PRODUCT_SYSTEM_EXT_PROPERTIES += \
    persist.sys.oplus.anim_level=1 \
    persist.sys.oplus.region=ZA \
    ro.build.release_type=true \
    ro.oplus.camera.defercap.support=1 \
    ro.oplus.display.screenhole.positon=67,36:132,101 \
    ro.oplus.theme.version=16000 \
    ro.version.confidential=false \
    ro.build.version.module.sub_api=2 \
    ro.build.version.oplus.api=38 \
    ro.build.version.oplus.sub_api=47 \
    ro.build.version.oplusrom=V16.1.0 \
    ro.build.version.oplusrom.confidential=V16.1.0 \
    ro.build.version.oplusrom.display=16.0.8 \
    ro.oplus.fusionlight=true \
    ro.oplus.pipeline.region=IN \
    ro.oplus.product.series=flagship_series \
    ro.oplus.camera.defercap.all.quick.visible.support=1

# Vendor Camera Properties
PRODUCT_VENDOR_PROPERTIES += \
    persist.vendor.camera.privapp.list=com.oplus.camera,org.codeaurora.snapcam,lv.mcprotector.mcpro24fps \
    vendor.camera.aux.packageexcludelist=org.telegram.messenger,org.thunderdog.challegram,us.zoom.videomeetings \
    ro.vendor.oplus.market.enname=OnePlus\ 9\ 5G \
    ro.vendor.oplus.market.name=OnePlus\ 9\ 5G

# Product Camera Properties
PRODUCT_PRODUCT_PROPERTIES += \
    persist.vendor.camera.privapp.list=com.oplus.camera \
    ro.com.google.lens.oem_camera_package=com.oplus.camera \
    ro.com.google.lens.oem_image_package=com.oneplus.gallery \
    ro.oplus.camera.defercap.support=1 \
    ro.oplus.system.camera.name=com.oplus.camera \
    ro.oplus.camera.defercap.all.quick.visible.support=1 \
    ro.oplus.camera.livephoto.support=1 \
    ro.camera.disableHeicUltraHDR=1 \
    oplus.software.camera.10bit=1 \
    vendor.camera.aux.packagelist=com.oplus.camera \
    vendor.camera.skip_unconfigure.packagelist=com.oplus.camera \
    ro.oplus.camera.facing.front.need.disable.nfc=1 \
    ro.oplus.camera.portrait.center.switch=oplus.switch.portrait.center \
    ro.oplus.camera.portrait_center.prefix=oplus.portrait.center. \
    ro.oplus.camera.video.beauty.switch=oplus.switch.video.beauty \
    ro.oplus.camera.video_beauty.prefix=oplus.video.beauty. \
    ro.oplus.camera.speechassist=true \
    ro.oplus.system.camera.flashlight=com.oplus.motor.flashlight \
    ro.camera.privileged.3rdpartyApp=com.mediatek.expert.mtkcamhelper;com.aiunit.aon; \
    persist.camera.override_enable=true \
    persist.camera.override_preview_hdr_support=false \
    persist.logd.log.load.camerahalserver.lower_limit=1000 \
    persist.logd.log.load.camerahalserver.threshold=800000 \
    persist.logd.log.load.camerahalserver.upper_limit=3000 \
    persist.logd.log.load.com.oplus.camera.lower_limit=1000 \
    persist.logd.log.load.com.oplus.camera.threshold=800000 \
    persist.logd.log.load.com.oplus.camera.upper_limit=3000 \
    persist.logd.log.load.vendor.qti.camera.provider-service_64.lower_limit=500 \
    persist.logd.log.load.vendor.qti.camera.provider-service_64.threshold=400000 \
    persist.logd.log.load.vendor.qti.camera.provider-service_64.upper_limit=1500

# Photo
$(call soong_config_set,camera,package_name,com.oplus.packageName)
$(call soong_config_set,camera,allow_nonincreasing_timestamps,true)
$(call soong_config_set,libgui,num_buffer_slots,96)

# Video
$(call soong_config_set_bool,camera,override_format_from_reserved,true)

# Inherit definer package
$(call inherit-product, vendor/oplus/camera/definer/oplus-definer.mk)

# Inherit from camera-vendor.mk
$(call inherit-product, vendor/oplus/camera/camera-vendor.mk)

# SEpolicy
include vendor/oplus/camera/sepolicy/SEPolicy.mk
