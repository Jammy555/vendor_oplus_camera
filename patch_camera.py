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

def main():
    if len(sys.argv) < 2:
        print("Usage: patch_camera.py <decompiled_dir>")
        sys.exit(1)
    
    decompiled_dir = sys.argv[1]
    any_patched = False
    
    manifest_path = os.path.join(decompiled_dir, 'AndroidManifest.xml')
    if os.path.exists(manifest_path):
        print("--- Mode: Camera APK Patching ---")
        # 1. Patch AndroidManifest.xml
        if patch_file(manifest_path, patch_manifest): any_patched = True

        # 2. Dynamic walk and patch all target smali files
        for root, _, files in os.walk(decompiled_dir):
            for file in files:
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, decompiled_dir).replace('\\', '/')
                if relpath.endswith('d6/l2.smali'):
                    if patch_file(filepath, patch_typeface_util): any_patched = True
                elif relpath.endswith('f3/a.smali'):
                    if patch_file(filepath, patch_coui_theme_overlay): any_patched = True
                elif relpath.endswith('ExtensionRegistryLite.smali'):
                    if patch_file(filepath, patch_extension_registry): any_patched = True
                elif relpath.endswith('ml/b.smali'):
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



    if any_patched:
        print("Patches were applied/modified.")
        sys.exit(10)
    else:
        print("No patches needed to be applied.")
        sys.exit(0)

if __name__ == '__main__':
    main()
