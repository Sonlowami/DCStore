import chai from 'chai';
import {getData, postData, updateData} from '../../hooks/queryFromApi'
import axios from 'axios';

const expect = chai.expect;

describe('Testing getData', () => {
  let stubGetItem;
  let stubAxiosGet;
  beforeEach(() => {
    stubGetItem = sinon.stub(localStorage, 'getItem');
    stubAxiosGet = sinon.stub(axios, get);
    stubAxiosGet.returns({message: 'successful'});
  });
  afterEach(() => {
    stubGetItem.reset();
    stubAxiosGet.reset();
  });
  
  it('test getData gets token from localStorage', () => {
    stubGetItem.returns({'x-token': 'abc123'});
    getData('/patients', pageNumber=4);

    expect(stubGetItem.calledOnceWithExactly('/patients', 4)).to.be.true;
    expect(stubGetItem.returned({'x-token': 'abc123'})).to.be.true;
  });

  it('test if geData calls axios.get', () => {
    getData('/patients', pageNumber=4);
    expect(stubAxiosGet.calledOnceWithExactly('/patients', { params: 4 })).to.be.true;
    expect(stubAxiosGet.returned({message: 'successful'}));

  });

  it('test getData defaults pageNumber to 0', () => {
    getData('/patients');
    expect(stubGetItem.calledOnceWithExactly('/patients', 0)).to.be.true;
  });
  it('test getData calls axios with the x-token header', () => {
    stubGetItem.returns({'x-token': 'abc123'});
    getData('/patients');
    expect(stubAxiosGet.calledOnceWithExactly('/patients', {
      params: { pageNumber: 0 },
      headers: { 'x-token': 'abc123'}
    })).to.be.true;
  });
})
