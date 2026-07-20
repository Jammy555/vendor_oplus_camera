#!/usr/bin/env python3
import os
import re
import sys

def patch_file(file_path, patch_func):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return False
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content_normalized = content.replace('\r\n', '\n')
    new_content = patch_func(content_normalized)
    if new_content != content_normalized:
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        print(f"Patched: {file_path}")
        return True
    else:
        # No changes needed logically
        return False

def patch_typeface_util(content):
    # Match the method public static a(Landroid/content/Context;)Landroid/graphics/Typeface;
    pattern = r'(\.method public static a\(Landroid/content/Context;\)Landroid/graphics/Typeface;\s+\.locals \d+).*?(\.end method)'
    replacement = (
        r'\1\n\n'
        r'    sget-object v0, Landroid/graphics/Typeface;->DEFAULT:Landroid/graphics/Typeface;\n\n'
        r'    return-object v0\n'
        r'\2'
    )
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def patch_coui_theme_overlay(content):
    # Match the method public static c(Landroid/content/res/Configuration;)Loplus/content/res/OplusExtraConfiguration;
    pattern = r'(\.method public static c\(Landroid/content/res/Configuration;\)Loplus/content/res/OplusExtraConfiguration;\s+\.locals \d+).*?(\.end method)'
    replacement = (
        r'\1\n\n'
        r'    const/4 v0, 0x0\n\n'
        r'    return-object v0\n'
        r'\2'
    )
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def patch_extension_registry(content):
    # Match volatile eagerlyParseMessageSets:Z = false
    pattern = r'(\.field private static volatile eagerlyParseMessageSets:Z) = false'
    return re.sub(pattern, r'\1', content)

def patch_manifest(content):
    # Remove android:permission attributes containing oplus, sandbox, or remote.service
    pattern = r'\s+android:permission="[^"]*(?:oplus|sandbox|remote\.service|CAPTURE_PREVIEW)[^"]*"'
    return re.sub(pattern, '', content)

def strip_static_initialization(content):
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith(".field ") and " static " in line and " = " in line and " final " not in line:
            line = line.split(" = ")[0]
        new_lines.append(line)
    return "\n".join(new_lines)

def patch_sensor_wait(content):
    pattern = r'(\.method public isSensorModeNeedWait\(II\)Z\s+\.locals \d+).*?(\.end method)'
    replacement = (
        r'\1\n\n'
        r'    const/4 p0, 0x0\n\n'
        r'    return p0\n'
        r'\2'
    )
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def patch_facebeauty_path(content):
    return content.replace(
        '/product/lib64/libApsFaceBeautyPreviewProductJni.so',
        '/system_ext/lib64/libApsFaceBeautyPreviewProductJni.so'
    )

def patch_ml_b(content):
    if "# patch_ml_b" in content:
        return content
    pattern = re.compile(
        r'(invoke-virtual/range\s+\{v3\s+\.\.\s+v8\},\s+Landroid/content/ContentResolver;->query\(.*?\)\s*.*?\s*move-result-object\s+p0)\s*(.*?\s*goto\s+:goto_0)',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        body = match.group(1)
        rest = match.group(2)
        replacement = (
            f"    # patch_ml_b\n"
            f"    :try_start_0\n"
            f"    {body.strip()}\n"
            f"    :try_end_0\n"
            f"    .catch Ljava/lang/Exception; {{:try_start_0 .. :try_end_0}} :catch_0\n"
            f"    {rest.strip()}\n\n"
            f"    :catch_0\n"
            f"    const/4 p0, 0x0\n"
            f"    goto :goto_0"
        )
        content = content.replace(match.group(0), replacement)
    return content

def patch_c0_g(content):
    if "# patch_c0_g" in content:
        return content
    pattern = re.compile(
        r'(invoke-virtual/range\s+\{v1\s+\.\.\s+v6\},\s+Landroid/content/ContentResolver;->query\(.*?\)\s*.*?\s*move-result-object\s+p0)\s*(.*?\s*goto\s+:goto_0)',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        body = match.group(1)
        rest = match.group(2)
        replacement = (
            f"    # patch_c0_g\n"
            f"    :try_start_0\n"
            f"    {body.strip()}\n"
            f"    :try_end_0\n"
            f"    .catch Ljava/lang/Exception; {{:try_start_0 .. :try_end_0}} :catch_0\n"
            f"    {rest.strip()}\n\n"
            f"    :catch_0\n"
            f"    const/4 p0, 0x0\n"
            f"    goto :goto_0"
        )
        content = content.replace(match.group(0), replacement)
    return content

def patch_thread_monitor(content):
    pattern = r'(\.method public final run\(\)V\s+\.locals \d+).*?(\.end method)'
    replacement = (
        r'\1\n\n'
        r'    return-void\n'
        r'\2'
    )
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def patch_ah_a(content):
    return content.replace('if-nez p0, :cond_2', 'goto :cond_2')

def patch_provider_utils(content):
    if "# patch_provider_utils" in content:
        return content
    # Call
    pattern_call = re.compile(
        r'(invoke-virtual\s+\{p0,\s+v0,\s+p1,\s+v1,\s+p2\},\s+Landroid/content/ContentResolver;->call\(Ljava/lang/String;\s*Ljava/lang/String;\s*Ljava/lang/String;\s*Landroid/os/Bundle;\)Landroid/os/Bundle;.*?move-result-object\s+p0)\s*(.*?\s*return-object\s+p0)',
        re.DOTALL
    )
    match_call = pattern_call.search(content)
    if match_call:
        body = match_call.group(1)
        rest = match_call.group(2)
        replacement = (
            f"    # patch_provider_utils\n"
            f"    :try_start_0\n"
            f"    {body.strip()}\n"
            f"    :try_end_0\n"
            f"    .catch Ljava/lang/Exception; {{:try_start_0 .. :try_end_0}} :catch_0\n"
            f"    {rest.strip()}\n\n"
            f"    :catch_0\n"
            f"    const/4 p0, 0x0\n"
            f"    return-object p0"
        )
        content = content.replace(match_call.group(0), replacement)

    # Query
    pattern_query = re.compile(
        r'(invoke-virtual\s+\{p0,\s+p1,\s+p2,\s+v0,\s+p2\},\s+Landroid/content/ContentResolver;->query\(.*?\)Landroid/database/Cursor;.*?move-result-object\s+p0)\s*(.*?\s*invoke-static\s+\{p0\},\s+Lcom/oplus/epona/ipc/cursor/ProviderCursor;->stripBundle\(Landroid/database/Cursor;\)Landroid/os/Bundle;.*?move-result-object\s+p0\s*.*?\s*return-object\s+p0)',
        re.DOTALL
    )
    match_query = pattern_query.search(content)
    if match_query:
        body = match_query.group(1)
        rest = match_query.group(2)
        replacement = (
            f"    # patch_provider_utils\n"
            f"    :try_start_1\n"
            f"    {body.strip()}\n"
            f"    :try_end_1\n"
            f"    .catch Ljava/lang/Exception; {{:try_start_1 .. :try_end_1}} :catch_1\n"
            f"    {rest.strip()}\n\n"
            f"    :catch_1\n"
            f"    const/4 p0, 0x0\n"
            f"    return-object p0"
        )
        content = content.replace(match_query.group(0), replacement)
    return content

def patch_camera_characteristics_wrapper(content):
    if "MockHelper" in content:
        return content
    pattern = r'(\.method public get\(Landroid/hardware/camera2/CameraCharacteristics\$Key;\)Ljava/lang/Object;\s+\.locals 5)'
    replacement = (
        r'\1\n\n'
        r'    iget-object v0, p0, Lcom/oplus/ocs/camera/producer/info/CameraCharacteristicsWrapper;->mCameraId:Ljava/lang/String;\n\n'
        r'    invoke-static {p1, v0}, Lcom/oplus/ocs/camera/producer/info/MockHelper;->getMockValue(Landroid/hardware/camera2/CameraCharacteristics$Key;Ljava/lang/String;)Ljava/lang/Object;\n\n'
        r'    move-result-object v0\n\n'
        r'    if-eqz v0, :cond_mock_null\n\n'
        r'    return-object v0\n\n'
        r'    :cond_mock_null'
    )
    return re.sub(pattern, replacement, content, count=1)

def write_mock_helper(decompiled_dir):
    mock_helper_dir = os.path.join(decompiled_dir, 'smali', 'com', 'oplus', 'ocs', 'camera', 'producer', 'info')
    os.makedirs(mock_helper_dir, exist_ok=True)
    mock_helper_path = os.path.join(mock_helper_dir, 'MockHelper.smali')
    smali_content = """#
.class public Lcom/oplus/ocs/camera/producer/info/MockHelper;
.super Ljava/lang/Object;
.source "MockHelper.java"


# direct methods
.method public static getMockValue(Landroid/hardware/camera2/CameraCharacteristics$Key;Ljava/lang/String;)Ljava/lang/Object;
    .locals 6
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/hardware/camera2/CameraCharacteristics$Key",
            "<*>;",
            "Ljava/lang/String;",
            ")",
            "Ljava/lang/Object;"
        }
    .end annotation

    const/4 v0, 0x0

    if-nez p0, :cond_0

    return-object v0

    :cond_0
    invoke-virtual {p0}, Landroid/hardware/camera2/CameraCharacteristics$Key;->getName()Ljava/lang/String;

    move-result-object v1

    if-nez v1, :cond_1

    return-object v0

    :cond_1
    const-string v2, "com.oplus.supported.cameraid.type"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    const/4 v3, 0x1

    const/4 v4, 0x0

    if-eqz v2, :cond_8

    invoke-static {}, Lcom/oplus/ocs/camera/producer/info/MockHelper;->hasCamera5()Z

    move-result v5

    const-string v2, "0"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_2

    new-array v0, v3, [I

    aput v4, v0, v4

    return-object v0

    :cond_2
    const-string v2, "1"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_3

    new-array v0, v3, [I

    aput v3, v0, v4

    return-object v0

    :cond_3
    const-string v2, "2"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_4

    new-array v0, v3, [I

    const/4 v1, 0x2

    aput v1, v0, v4

    return-object v0

    :cond_4
    const-string v2, "3"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_5

    new-array v0, v3, [I

    if-eqz v5, :cond_99

    const/4 v1, 0x6

    aput v1, v0, v4

    return-object v0

    :cond_99
    const/16 v1, 0xd

    aput v1, v0, v4

    return-object v0

    :cond_5
    const-string v2, "4"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_6

    new-array v0, v3, [I

    if-eqz v5, :cond_9a

    const/16 v1, 0xd

    aput v1, v0, v4

    return-object v0

    :cond_9a
    const/16 v1, 0xc

    aput v1, v0, v4

    return-object v0

    :cond_6
    const-string v2, "5"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_7

    new-array v0, v3, [I

    const/16 v1, 0xc

    aput v1, v0, v4

    return-object v0

    :cond_7
    return-object v0

    :cond_8
    const-string v2, "org.codeaurora.qcamera3.logicalCameraType.logical_camera_type"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_10

    const-string v2, "com.oplus.logical.camera.type"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_12

    :cond_10
    invoke-static {}, Lcom/oplus/ocs/camera/producer/info/MockHelper;->hasCamera5()Z

    move-result v5

    const-string v2, "5"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_11

    new-array v0, v3, [I

    aput v3, v0, v4

    return-object v0

    :cond_11
    if-nez v5, :cond_12

    const-string v5, "4"

    invoke-virtual {v5, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_12

    new-array v0, v3, [I

    aput v3, v0, v4

    return-object v0

    :cond_12
    const-string v2, "com.oplus.custom.zoom.range"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_20

    const-string v2, "com.oplus.expert.zoom.range"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_25

    :cond_20
    invoke-static {}, Lcom/oplus/ocs/camera/producer/info/MockHelper;->hasCamera5()Z

    move-result v5

    if-eqz v5, :cond_21

    const-string v2, "5"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_22

    goto :goto_sat

    :cond_21
    const-string v2, "4"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_22

    :goto_sat
    const/4 v0, 0x4

    new-array v0, v0, [F

    fill-array-data v0, :array_sat

    return-object v0

    :cond_22
    const/4 v0, 0x4

    new-array v0, v0, [F

    fill-array-data v0, :array_normal

    return-object v0

    :cond_25
    return-object v0

    :array_sat
    .array-data 4
        0x3f19999a    # 0.6f
        0x41200000    # 10.0f
        0x3f800000    # 1.0f
        0x40000000    # 2.0f
    .end array-data

    :array_normal
    .array-data 4
        0x3f800000    # 1.0f
        0x41200000    # 10.0f
        0x3f800000    # 1.0f
        0x3f800000    # 1.0f
    .end array-data
.end method

.method private static hasCamera5()Z
    .locals 6

    const/4 v0, 0x0

    :try_start_0
    invoke-static {}, Landroid/app/ActivityThread;->currentApplication()Landroid/app/Application;

    move-result-object v1

    if-nez v1, :cond_0

    return v0

    :cond_0
    const-string v2, "camera"

    invoke-virtual {v1, v2}, Landroid/app/Application;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/hardware/camera2/CameraManager;

    if-nez v1, :cond_1

    return v0

    :cond_1
    invoke-virtual {v1}, Landroid/hardware/camera2/CameraManager;->getCameraIdList()[Ljava/lang/String;

    move-result-object v1

    array-length v2, v1

    const/4 v3, 0x0

    :goto_0
    if-ge v3, v2, :cond_3

    aget-object v4, v1, v3

    const-string v5, "5"

    invoke-virtual {v5, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    if-eqz v4, :cond_2

    const/4 v0, 0x1

    return v0

    :cond_2
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    :catch_0
    :cond_3
    return v0
.end method
"""
    if os.path.exists(mock_helper_path):
        with open(mock_helper_path, 'r', encoding='utf-8') as f:
            existing = f.read()
        if existing == smali_content:
            print(f"No changes needed: {mock_helper_path}")
            return False
    with open(mock_helper_path, 'w', encoding='utf-8') as f:
        f.write(smali_content)
    print(f"Created/Modified: {mock_helper_path}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: patch_camera.py <decompiled_dir>")
        sys.exit(1)
    
    decompiled_dir = sys.argv[1]
    any_patched = False
    
    manifest_path = os.path.join(decompiled_dir, 'AndroidManifest.xml')
    if os.path.exists(manifest_path):
        print("--- Mode: Camera APK Patching ---")
        # 1. Patch TypefaceUtil (smali/d6/l2.smali)
        typeface_path = os.path.join(decompiled_dir, 'smali', 'd6', 'l2.smali')
        if patch_file(typeface_path, patch_typeface_util): any_patched = True
        
        # 2. Patch COUIThemeOverlay (smali/f3/a.smali)
        theme_path = os.path.join(decompiled_dir, 'smali', 'f3', 'a.smali')
        if patch_file(theme_path, patch_coui_theme_overlay): any_patched = True
        
        # 3. Patch ExtensionRegistryLite (smali_classes23/com/google/protobuf/ExtensionRegistryLite.smali)
        proto_path = os.path.join(decompiled_dir, 'smali_classes23', 'com', 'google', 'protobuf', 'ExtensionRegistryLite.smali')
        if patch_file(proto_path, patch_extension_registry): any_patched = True
        
        # 4. Patch AndroidManifest.xml
        if patch_file(manifest_path, patch_manifest): any_patched = True

        # 5. Dynamic walk and patch custom ROM compatibility fixes
        for root, _, files in os.walk(decompiled_dir):
            for file in files:
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, decompiled_dir)
                if relpath.endswith('ml/b.smali'):
                    if patch_file(filepath, patch_ml_b): any_patched = True
                elif relpath.endswith('c0/g.smali'):
                    if patch_file(filepath, patch_c0_g): any_patched = True
                elif relpath.endswith('u6/e.smali'):
                    if patch_file(filepath, patch_thread_monitor): any_patched = True
                elif relpath.endswith('ah/a.smali'):
                    if patch_file(filepath, patch_ah_a): any_patched = True
                elif relpath.endswith('com/oplus/epona/utils/ProviderUtils.smali'):
                    if patch_file(filepath, patch_provider_utils): any_patched = True
    else:
        print("--- Mode: SDK Jar Patching ---")
        # Recursively find all .smali files and strip static assignments
        for root, _, files in os.walk(decompiled_dir):
            for file in files:
                if file.endswith('.smali') and file != 'MockHelper.smali':
                    smali_path = os.path.join(root, file)
                    if patch_file(smali_path, strip_static_initialization): any_patched = True
        
        # Patch BaseMode.smali sensor wait
        basemode_path = os.path.join(decompiled_dir, 'smali', 'com', 'oplus', 'ocs', 'camera', 'producer', 'mode', 'BaseMode.smali')
        if os.path.exists(basemode_path):
            if patch_file(basemode_path, patch_sensor_wait): any_patched = True
            
        # Patch OplusFaceBeautyPreview.smali product lib path
        facebeauty_path = os.path.join(decompiled_dir, 'smali', 'com', 'oplus', 'camera', 'facebeauty', 'OplusFaceBeautyPreview.smali')
        if os.path.exists(facebeauty_path):
            if patch_file(facebeauty_path, patch_facebeauty_path): any_patched = True

        # Patch CameraCharacteristicsWrapper
        wrapper_path = os.path.join(decompiled_dir, 'smali', 'com', 'oplus', 'ocs', 'camera', 'producer', 'info', 'CameraCharacteristicsWrapper.smali')
        if os.path.exists(wrapper_path):
            if patch_file(wrapper_path, patch_camera_characteristics_wrapper): any_patched = True
            if write_mock_helper(decompiled_dir): any_patched = True

    if any_patched:
        print("Patches were applied/modified.")
        sys.exit(10)
    else:
        print("No patches needed to be applied.")
        sys.exit(0)

if __name__ == '__main__':
    main()
