#include <iostream>
#include <string>
#include <unordered_map>
#include <deque>

using namespace std::literals;

struct Costant {
    Costant() = delete;
    constexpr static int DAY_SECONDS = 86400;
    constexpr static std::string_view BOOK = "BOOK"sv;
    constexpr static std::string_view CLIENTS = "CLIENTS"sv;
    constexpr static std::string_view ROOMS = "ROOMS"sv;
};

struct Booking {
    std::string hotel_name;
    int64_t time;
    uint32_t client_id;
    uint16_t room_count;
};

class Hotel {
public:

    void addBooking(const Booking& booking) {
        totalRoomCount += booking.room_count;
        clients[booking.client_id] += 1;
    }

    void removeBooking(const Booking& booking) {
        totalRoomCount -= booking.room_count;
        clients[booking.client_id] -= 1;
        if (clients[booking.client_id] == 0) {
            clients.erase(booking.client_id);
        }
    }

    int getClientCount() const {
        return clients.size();
    }

    int getRoomCount() const {
        return totalRoomCount;
    }

private:
    int totalRoomCount = 0;
    std::unordered_map<uint32_t, int> clients;  // храним клиентов для отеля
};

class HotelsManager {
public:
    void book(const std::string& hotel_name, int64_t time, uint32_t client_id, uint16_t room_count) {
        // удаляем устаревшие бронирования (прошедшие сутки)
        while (!bookings.empty() && bookings.begin()->time <= time - Costant::DAY_SECONDS) {
            const Booking& old_booking = *bookings.begin();
            hotels[old_booking.hotel_name].removeBooking(old_booking);
            bookings.pop_front();
        }

        // добавляем новое бронирование
        bookings.push_back({hotel_name, time, client_id, room_count});
        hotels[hotel_name].addBooking(*bookings.rbegin());
    }

    int getClientCount(const std::string& hotel_name) {
        return hotels[hotel_name].getClientCount();
    }

    int getRoomCount(const std::string& hotel_name) {
        return hotels[hotel_name].getRoomCount();
    }

private:
    std::deque<Booking> bookings;
    std::unordered_map<std::string, Hotel> hotels;
};


int main() {
    HotelsManager manager;

    int Q;
    std::cin >> Q;

    for (int i = 0; i < Q; ++i) {
        std::string action;
        std::cin >> action;

        if (action == Costant::BOOK) {
            int64_t time;
            uint32_t client_id;
            uint16_t room_count;
            std::string hotel_name;
            std::cin >> time >> hotel_name >> client_id >> room_count;
            manager.book(hotel_name, time, client_id, room_count);
        } else if (action == Costant::CLIENTS) {
            std::string hotel_name;
            std::cin >> hotel_name;
            std::cout << manager.getClientCount(hotel_name) << std::endl;
        } else if (action == Costant::ROOMS) {
            std::string hotel_name;
            std::cin >> hotel_name;
            std::cout << manager.getRoomCount(hotel_name) << std::endl;
        }
    }

    return 0;
}
