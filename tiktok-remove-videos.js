const maxDelete = 100; // Összesen hány videót töröljön
let deletedCount = 0;

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Várakozás a Menü Törlés gombra JS-sel szövegellenőrzéssel
async function waitForDeleteMenu(timeout = 10000) {
    const interval = 200;
    let elapsed = 0;
    while (elapsed < timeout) {
        const candidates = document.querySelectorAll('div[data-tt="components_ActionCell_FlexRow"]');
        for (const el of candidates) {
            if (el.innerText.includes("Törlés")) return el;
        }
        await sleep(interval);
        elapsed += interval;
    }
    return null;
}

// Várakozás bármely selectorra
async function waitForSelector(selector, timeout = 10000) {
    const interval = 200;
    let elapsed = 0;
    while (elapsed < timeout) {
        const el = document.querySelector(selector);
        if (el) return el;
        await sleep(interval);
        elapsed += interval;
    }
    return null;
}

async function deleteOne() {
    // Második parentRow
    const postContainers = document.querySelectorAll('div[data-tt="components_PostTable_Container"]');
    if (postContainers.length < 2) {
        console.log("Második PostTable Container nem található!");
        return false;
    }
    const parentRow = postContainers[1];

    // 1️⃣ 3 pötty
    const threeDotButton = parentRow.querySelector('button[data-tt="components_ActionCell_Clickable"]');
    if (!threeDotButton) {
        console.log("3 pötty gomb nem található!");
        return false;
    }
    threeDotButton.click();
    console.log("3 pötty gombra kattintva.");
    await sleep(5000);

    // 2️⃣ Menü Törlés gomb
    const menuButtonParent = await waitForDeleteMenu(10000);
    if (!menuButtonParent) {
        console.log("Menü Törlés gomb nem jelent meg időben!");
        return false;
    }
    menuButtonParent.click();
    console.log("Menü Törlés gombra kattintva.");
    await sleep(5000);

    // 3️⃣ Popup Törlés gomb
    const modalDeleteButton = await waitForSelector('div[data-tt="components_Modal_FlexItem"] button[data-tt="components_Modal_TUXButton"]', 10000);
    if (!modalDeleteButton) {
        console.log("Popup Törlés gomb nem található!");
        return false;
    }
    modalDeleteButton.click();
    deletedCount++;
    console.log(`Popup Törlés gombra kattintva. Összesen törölve: ${deletedCount}`);
    await sleep(5000);

    return true;
}

// Fő ciklus: 5-ször törlés, 10 mp szünetekkel
async function runDeletes() {
    while (deletedCount < maxDelete) {
        console.log(`▶️ Következő törlés (${deletedCount + 1}/${maxDelete})`);
        const success = await deleteOne();
        if (!success) {
            console.log("❌ Törlés sikertelen, megáll a script.");
            break;
        }

        if (deletedCount < maxDelete) {
            console.log("⏳ 10 másodperces szünet következik...");
            await sleep(10000);
        }
    }
    console.log("✅ Minden törlés lefutott vagy a folyamat megszakadt.");
}

// Indítás
runDeletes();
