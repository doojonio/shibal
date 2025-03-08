

export function getLastHours(hours: number) {
    const now = new Date();
    // now.setHours(now.getHours() + Math.round(now.getMinutes() / 60));
    now.setMinutes(0, 0, 0);

    const lastHours: Date[] = [];

    for (let i = 0; i <= hours - 1; i++) {
        const hour = new Date(now.getTime() - (i * 60 * 60 * 1000));
        lastHours.push(hour);
    }

    return lastHours.reverse();
}

export function getLastDays(days: number) {
    const now = new Date();
    now.setMinutes(0, 0, 0);

    const lastDays: Date[] = [];

    for (let i = 0; i <= days - 1; i++) {
        const day = new Date(now.getTime() - (i * 24 * 60 * 60 * 1000));
        lastDays.push(day);
    }

    return lastDays.reverse();
}