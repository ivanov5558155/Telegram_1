import os
import re
import sys

SETTINGS_PATH   = "TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java"
USERCONFIG_PATH = "TMessagesProj/src/main/java/org/telegram/messenger/UserConfig.java"
MESSAGES_PATH   = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"

# WeryGramPremiumActivity — только стандартные Android виджеты, никаких RecyclerView
PREMIUM_ACTIVITY = """\
package org.telegram.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Typeface;
import android.view.Gravity;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.MessagesController;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;

public class WeryGramPremiumActivity extends BaseFragment {

    private static final String KEY_VISUAL_PREMIUM  = "visual_premium";
    private static final String KEY_VERIFIED        = "wery_verified";
    private static final String KEY_HIDE_ADS        = "wery_hide_ads";
    private static final String KEY_ANIM_EMOJI      = "wery_anim_emoji";
    private static final String KEY_PREM_STICKERS   = "wery_prem_stickers";
    private static final String KEY_PREM_REACTIONS  = "wery_prem_reactions";

    private static SharedPreferences prefs() {
        return MessagesController.getGlobalMainSettings();
    }
    private static boolean get(String key) { return prefs().getBoolean(key, false); }
    private static void set(String key, boolean v) { prefs().edit().putBoolean(key, v).apply(); }

    @Override
    public boolean onFragmentCreate() {
        super.onFragmentCreate();
        return true;
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setTitle("WeryGram Premium");
        actionBar.setAllowOverlayTitle(true);
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) finishFragment();
            }
        });

        FrameLayout root = new FrameLayout(context);
        root.setBackgroundColor(0xFFF0F0F0);
        fragmentView = root;

        ScrollView scroll = new ScrollView(context);
        root.addView(scroll, new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.MATCH_PARENT));

        LinearLayout container = new LinearLayout(context);
        container.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(container, new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.WRAP_CONTENT));

        // Заголовок секции
        TextView header = new TextView(context);
        header.setText("VIZUALNYE NASTROYKI");
        header.setTextSize(13);
        header.setTextColor(0xFF79879B);
        header.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(16),
            AndroidUtilities.dp(21), AndroidUtilities.dp(8));
        container.addView(header);

        // Строки тогглов
        addToggleRow(context, container, "Vizualno Telegram Premium", KEY_VISUAL_PREMIUM, new Runnable() {
            @Override public void run() {
                if (get(KEY_VISUAL_PREMIUM)) {
                    set(KEY_VERIFIED, true);
                    set(KEY_ANIM_EMOJI, true);
                    set(KEY_PREM_STICKERS, true);
                    set(KEY_PREM_REACTIONS, true);
                }
            }
        });
        addToggleRow(context, container, "Galocka verifikacii", KEY_VERIFIED, null);
        addToggleRow(context, container, "Skryt reklamu", KEY_HIDE_ADS, null);
        addToggleRow(context, container, "Animirovannye emoji", KEY_ANIM_EMOJI, null);
        addToggleRow(context, container, "Premium stikery", KEY_PREM_STICKERS, null);
        addToggleRow(context, container, "Rasshirennye reakcii", KEY_PREM_REACTIONS, null);

        return fragmentView;
    }

    private void addToggleRow(Context ctx, LinearLayout parent,
                               String label, final String key, final Runnable onEnable) {
        LinearLayout row = new LinearLayout(ctx);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setBackgroundColor(0xFFFFFFFF);
        row.setPadding(AndroidUtilities.dp(21), AndroidUtilities.dp(14),
            AndroidUtilities.dp(21), AndroidUtilities.dp(14));

        TextView tv = new TextView(ctx);
        tv.setText(label);
        tv.setTextSize(16);
        tv.setTextColor(0xFF000000);
        LinearLayout.LayoutParams tvParams = new LinearLayout.LayoutParams(
            0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
        row.addView(tv, tvParams);

        final Switch sw = new Switch(ctx);
        sw.setChecked(get(key));
        sw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                set(key, isChecked);
                if (isChecked && onEnable != null) onEnable.run();
                if (getParentActivity() != null)
                    Toast.makeText(getParentActivity(),
                        label + (isChecked ? ": ON" : ": OFF"),
                        Toast.LENGTH_SHORT).show();
            }
        });
        row.addView(sw);

        // Разделитель
        View divider = new View(ctx);
        divider.setBackgroundColor(0xFFE0E0E0);
        LinearLayout.LayoutParams dp = new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT, 1);
        dp.setMarginStart(AndroidUtilities.dp(21));

        parent.addView(row);
        parent.addView(divider, dp);
    }
}
"""


def patch_settings(code):
    code = re.sub(r'case 9999:.*?break;', '', code, flags=re.DOTALL)
    code = re.sub(r'items\.add\(SettingCell\.Factory\.of\(9999,[\s\S]*?\);\s*', '', code)
    code = re.sub(r'items\.add\(UItem\.asCheck\(9999,[\s\S]*?\);\s*', '', code)

    BUTTON = ('items.add(SettingCell.Factory.of(9999, 0xFF55CA47, 0xFF27B434, '
              'R.drawable.msg_settings, "WeryGram Premium"));')

    match = re.search(r'(items\.add\([\s\S]*?[nN]otif[\s\S]*?\);)', code)
    if match:
        anchor = match.group(1)
        code = code.replace(anchor, f'{BUTTON}\n        {anchor}', 1)
        print("OK Knopka dobavlena v nachalo nastroek.")
    else:
        code = code.replace("switch (item.id) {",
            f"{BUTTON}\n        switch (item.id) {{", 1)
        print("OK Knopka dobavlena rezervnym metodom.")

    CLICK = """\
case 9999: {
            presentFragment(new org.telegram.ui.WeryGramPremiumActivity());
            break;
        }"""
    if "switch (item.id) {" in code:
        code = code.replace("switch (item.id) {",
            f"switch (item.id) {{\n            {CLICK}", 1)
        print("OK Obrabotchik klika dobavlen.")
    return code


def patch_userconfig(code):
    if "visual_premium" in code:
        print("INFO UserConfig uzhe spatcherovan.")
        return code
    anchor = "public TLRPC.User getCurrentUser() {"
    if anchor not in code:
        print("WARN getCurrentUser() ne najden.")
        return code
    injection = """\
public TLRPC.User getCurrentUser() {
        if (currentUser != null &&
                org.telegram.messenger.MessagesController.getGlobalMainSettings()
                    .getBoolean("visual_premium", false)) {
            currentUser.premium  = true;
            currentUser.verified = true;
        }"""
    code = code.replace(anchor, injection, 1)
    print("OK UserConfig spatcherovan.")
    return code


def patch_messages_controller(code):
    if "visual_premium" in code:
        print("INFO MessagesController uzhe spatcherovan.")
        return code
    OLD = (
        "public TLRPC.User getUser(Long id) {\n"
        "        if (id == 0) {\n"
        "            return UserConfig.getInstance(currentAccount).getCurrentUser();\n"
        "        }\n"
        "        return users.get(id);\n"
        "    }"
    )
    NEW = """\
public TLRPC.User getUser(Long id) {
        if (id == 0) {
            return UserConfig.getInstance(currentAccount).getCurrentUser();
        }
        TLRPC.User user = users.get(id);
        if (user != null && id != null &&
                id.equals(UserConfig.getInstance(currentAccount).getClientUserId())) {
            if (MessagesController.getGlobalMainSettings()
                    .getBoolean("visual_premium", false)) {
                user.premium  = true;
                user.verified = true;
            }
        }
        return user;
    }"""
    if OLD in code:
        print("OK MessagesController spatcherovan.")
        return code.replace(OLD, NEW, 1)
    patched = re.sub(
        r'public TLRPC\.User getUser\(Long\s+(\w+)\)\s*\{'
        r'\s*if\s*\(\1\s*==\s*0\)\s*\{'
        r'\s*return\s+UserConfig\.getInstance\(currentAccount\)\.getCurrentUser\(\);\s*\}'
        r'\s*return\s+(\w+)\.get\(\1\);\s*\}',
        r'''public TLRPC.User getUser(Long \1) {
        if (\1 == 0) {
            return UserConfig.getInstance(currentAccount).getCurrentUser();
        }
        TLRPC.User user = \2.get(\1);
        if (user != null && \1 != null &&
                \1.equals(UserConfig.getInstance(currentAccount).getClientUserId())) {
            if (MessagesController.getGlobalMainSettings()
                    .getBoolean("visual_premium", false)) {
                user.premium  = true;
                user.verified = true;
            }
        }
        return user;
    }''', code)
    if patched != code:
        print("OK MessagesController spatcherovan (regex).")
    else:
        print("WARN getUser() ne najden.")
    return patched


def run():
    print("WeryGram Premium Patcher v4.0\n")
    if not os.path.exists(SETTINGS_PATH):
        print(f"ERROR: {SETTINGS_PATH} ne najden")
        sys.exit(1)

    with open(SETTINGS_PATH, "r", encoding="utf-8") as f: code = f.read()
    code = patch_settings(code)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f: f.write(code)

    if os.path.exists(USERCONFIG_PATH):
        with open(USERCONFIG_PATH, "r", encoding="utf-8") as f: uc = f.read()
        uc = patch_userconfig(uc)
        with open(USERCONFIG_PATH, "w", encoding="utf-8") as f: f.write(uc)

    if os.path.exists(MESSAGES_PATH):
        with open(MESSAGES_PATH, "r", encoding="utf-8") as f: mc = f.read()
        mc = patch_messages_controller(mc)
        with open(MESSAGES_PATH, "w", encoding="utf-8") as f: f.write(mc)

    MODULE_DIRS = [
        "TMessagesProj/src/main/java/org/telegram/ui",
        "TMessagesProj_App/src/main/java/org/telegram/ui",
        "TMessagesProj_AppHockeyApp/src/main/java/org/telegram/ui",
        "TMessagesProj_AppHuawei/src/main/java/org/telegram/ui",
        "TMessagesProj_AppStandalone/src/main/java/org/telegram/ui",
    ]
    found = set(MODULE_DIRS)
    for root, dirs, _ in os.walk("."):
        norm = root.replace(os.sep, "/").lstrip("./")
        if norm.endswith("org/telegram/ui") and "/src/main/java/" in norm:
            found.add(norm)

    for ui_dir in sorted(found):
        os.makedirs(ui_dir, exist_ok=True)
        out = os.path.join(ui_dir, "WeryGramPremiumActivity.java")
        with open(out, "w", encoding="utf-8") as f:
            f.write(PREMIUM_ACTIVITY)
        print(f"OK -> {out}")

    print("\nVSE MODULI USPESHNO MODIFICIROVANY!")


if __name__ == "__main__":
    run()
    
