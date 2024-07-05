from app.logic.use_cases.balance_history import GetMyBalanceHistory
from app.logic.abstract import BalanceHistoryAllSelector
from app.logic.models import BalanceChange
from app.utils.funcs import get_current_time

MOCK_DATA = {
    123: BalanceChange(1, 12.3, 2, get_current_time()),
    55: BalanceChange(2, 517.0, 1, get_current_time()),
}


class MockBalanceHistoryAllSelector(BalanceHistoryAllSelector):
    async def select_all_user_history(
        self, user_id: int
    ) -> list[BalanceChange]:
        return MOCK_DATA[user_id]


async def test_get_my_balance_history() -> None:
    use_case = GetMyBalanceHistory(MockBalanceHistoryAllSelector())
    assert await use_case(123) == MOCK_DATA[123]

    use_case = GetMyBalanceHistory(MockBalanceHistoryAllSelector())
    assert await use_case(55) == MOCK_DATA[55]
